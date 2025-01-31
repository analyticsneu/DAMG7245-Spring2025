from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Models
class User(BaseModel):
    name: str
    age: int

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Basic FastAPI Application!"}

@app.post("/greet")
def greet_user(user: User):
    if user.age < 18:
        return {"message": f"Hello, {user.name}! You're a minor."}
    else:
        return {"message": f"Hello, {user.name}! Welcome to adulthood."}

@app.get("/square/{number}")
def square_number(number: int):
    return {"number": number, "square": number ** 2}


# In-memory "database"
items_db = []

# Models
class Item(BaseModel):
    id: int
    name: str
    price: float
    description: str = None


# Endpoints
@app.get("/items", response_model=List[Item])
def get_items():
    """GET: Retrieve all items"""
    return items_db

@app.post("/items", response_model=Item)
def create_item(item: Item):
    """POST: Add a new item"""
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    """PUT: Update an existing item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db[i] = updated_item
            return updated_item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """DELETE: Remove an item"""
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return {"message": f"Item with ID {item_id} has been deleted"}

