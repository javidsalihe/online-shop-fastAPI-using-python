import dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import dotenv
import os
import requests


class Product(BaseModel):
    name: str
    price: float
    stock: int

class CardItem(BaseModel):
    product_id: int
    quantity: int

app = FastAPI()
products = [
    {"id": 1,"name": "laptop","price":2000,"stock":10},
    {"id": 2,"name": "mouse","price":150,"stock":200},
    {"id": 3,"name": "keyboard","price":270,"stock":34},
    {"id": 4,"name": "CPU","price":70,"stock":15}
]

cart = []


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return product
    else:
        return {"error": "Product not found"}




@app.post("/products")
def create_product(product: Product):
    new_product = product.dict()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    return new_product



@app.put("/products/{product_id}")
def update_product(product_id:int,product: Product):
    existing = next((p for p in products if p["id"] == product_id), None)
    if existing:
        existing["name"] = product.name
        existing["price"] = product.price
        existing["stock"] = product.stock
        return existing
    return {"error": "Product not found"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id),None)
    if product:
        products.remove(product)
        return {"success": True}
    return {"error": "Product not found"}



@app.post("/cards")
def add_to_card(item: CardItem):
    product = next((p for p in products if p["id"] == item.product_id),None)
    if product["stock"] < item.quantity:
        return {"error": "Not enough stock"}
    if not product:
        return {"error": "Product not found"}

    product["stock"] -= item.quantity
    cart.append({"product_id": item.product_id, "quantity": item.quantity, "name": product["name"], "price": product["price"]})
    return {"success": True}


@app.get("/cart")
def get_cart():
    total = sum(item["price"] * item["quantity"] for item in cart)
    return {"cart": cart, "total": total}


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    item = next((i for i in cart if i["product_id"] == product_id), None)
    if not item:
        return {"error": "not found"}
    cart.remove(item)
    product = next((p for p in products if p["id"] == product_id), None)
    product["stock"] += item["quantity"]
    return {"message":"deleted", "cart": cart}
