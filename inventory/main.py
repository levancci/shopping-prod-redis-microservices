from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel  
from dotenv import load_dotenv
import redis, os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)


import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

class Product(HashModel, index=True):
    name: str
    price: float
    quantity: int

    class Meta:
        database = r
    
@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

@app.post("/products")
def create(product: Product):
    return product.save()

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity 
    }

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk: str):
    product = Product.get(pk)
    product.delete(pk)