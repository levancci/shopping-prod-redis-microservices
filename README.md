# Microservices Course Demo

This project demonstrates a small event-driven microservices pattern using FastAPI, Redis, and Redis Streams. It models a simple e-commerce flow where an order is placed, inventory is checked, and compensating actions are triggered if a product disappears during the order process.

## Overview

The application is split into two main services:

- Inventory service: manages products and stock
- Payment service: creates orders and tracks payment/order status

A third frontend app allows a user to place orders from the browser.

## Architecture

### Inventory service
Location: `inventory/`

Responsibilities:
- Store product data in Redis OM models
- Expose product endpoints
- Handle product deletion
- Consume `order_completed` events from Redis Streams
- Reduce product quantity when a product is sold
- If the product is missing, publish a refund event for the payment service

### Payment service
Location: `payment/`

Responsibilities:
- Store orders in Redis OM models
- Create new orders
- Simulate order completion after a short delay
- Publish `order_completed` events to Redis
- Consume `refund_order` events from Redis Streams
- Mark orders as `refunded` when inventory determines the product is no longer available

### Frontend
Location: `frontend/inventory-frontend/`

Responsibilities:
- Create a simple checkout UI
- Fetch product details
- Send order creation requests to the payment API

## Redis event flow

The project uses Redis Streams to coordinate state between services.

1. Customer submits an order to the payment service.
2. The payment service creates an order with status `pending`.
3. After a brief delay, the payment service publishes an event on the `order_completed` stream.
4. The inventory consumer reads that event and tries to reduce stock for the product.
5. If the product no longer exists, inventory publishes a `refund_order` event.
6. The payment consumer reads the refund event and changes the order status from `pending` to `refunded`.

This is a simple example of eventual consistency and compensating actions in distributed systems.

## Project structure

```text
MicroServicesCourse/
├── inventory/
│   ├── consumer.py
│   ├── main.py
│   └── ...
├── payment/
│   ├── consumer.py
│   ├── main.py
│   └── ...
├── frontend/
│   └── inventory-frontend/
│       └── src/
├── main.py
├── pyproject.toml
├── README.md
└── .venv/
```

## Requirements

- Python 3.11+
- Redis instance with a reachable host and credentials
- FastAPI, Redis, Redis OM, and Requests
- Node.js and npm for the frontend app

The dependencies are defined in `pyproject.toml`.

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -U pip
pip install fastapi redis redis-om requests uvicorn[standard]
```

### 3. Start the inventory API

```bash
cd inventory
uvicorn main:app --reload --port 8000
```

### 4. Start the payment API

```bash
cd payment
uvicorn main:app --reload --port 8001
```

### 5. Start the Redis consumers

Open two terminals and run:

```bash
cd inventory
python consumer.py
```

```bash
cd payment
python consumer.py
```

### 6. Start the frontend

```bash
cd frontend/inventory-frontend
npm install
npm start
```

## Example workflow

1. Create a product in the inventory service.
2. Open the frontend and place an order.
3. Delete the product while the order is still in the pending window.
4. The inventory consumer handles the `order_completed` event and notices the product is gone.
5. The refund event is published.
6. The payment consumer marks the order as `refunded`.

## Important notes

### Redis Streams and `MKSTREAM`

If a consumer group is created for a Redis stream that does not already exist, Redis will fail unless the stream is created at the same time. In Python, this is usually done with `mkstream=True` when calling `xgroup_create`.

This matters in this project because the refund stream is created only after a refund event is published. Without creating the stream and group first, the consumer can loop with `NOGROUP` errors.

### Production readiness concerns

This project is a learning/demo setup and has a few important production gaps:

- Redis credentials are hardcoded in the source
- There is no real authentication or authorization layer
- The background task and stream consumer pattern is intentionally simple
- Error handling is minimal and designed for demonstration, not production reliability

## Useful troubleshooting tips

- Check whether both consumers are still running
- Confirm the Redis stream names match exactly: `order_completed` and `refund_order`
- Verify the product was deleted before the payment completion callback finalizes the order
- Make sure the consumer group is created with `mkstream=True` when the stream is not yet present
- Inspect Redis command output for `NOGROUP`, `BUSYGROUP`, or missing stream errors

## Summary

This example combines:
- FastAPI microservices
- Redis OM models
- Redis Streams for event-driven communication
- A compensating pattern for failed inventory updates

It is a simple but effective demonstration of how event-driven systems can handle race conditions between order placement and product deletion.
