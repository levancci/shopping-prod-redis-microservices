import { useState } from "react"; 
import { useEffect } from "react";

export const Orders = () => {
    const [id, setId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [message, setMessage] = useState('Buy your products here');

    useEffect( () => {
        (async () => {
            try {
                if (id) {
                    const response = await fetch(`http://localhost:8000/products/${id}`);
                    const content = await response.json();
                    const price = parseFloat(content.price) * 1.2;
                    setMessage(`You are buying ${content.name} for ${price} each. Available quantity: ${content.quantity}`);
                }
            }catch (e){
                setMessage('Error occurred while placing order. Please try again later');
            }
        })();
    }

    )

    const submit = async e => {
        e.preventDefault();
        await fetch('http://localhost:8001/orders', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id, 
                quantity
            })
        });
        setMessage('Thank you. Order placed successfully');
    }

    return <div className="container">
        <main>
            <div className="py-5 text-center">
                <h2>Checkout form</h2>
                <p className="lead">{message}</p>
            </div>


            <form onSubmit={submit}>
                <div className="row g-3">
                    <div className="col-md-6">
                        <label className="form-label">Product</label>
                        <input className="form-control" placeholder="Product" onChange={e => setId(e.target.value)} />
                    </div>

                    <div className="col-sm-6">
                        <label className="form-label">Quantity</label>
                        <input type="number" className="form-control" placeholder="Quantity" onChange={e => setQuantity(e.target.value)}/>
                    </div>
                </div>
            <hr className="my-4" />
            <button className="w-100 btn btn-primary btn-lg" type="submit">Place Order</button>
            </form>
        </main>
    </div>
}
