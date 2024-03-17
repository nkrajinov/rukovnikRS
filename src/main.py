from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice)
collection = db["ime_vase_kolekcije"]

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item:
        return item
    else:
        return {"message": "Item not found"}

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    result = collection.insert_one(item_dict)
    return {"message": "Item created successfully", "item_id": str(result.inserted_id)}

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    item_dict = item.dict()
    result = collection.replace_one({"_id": item_id}, item_dict)
    if result.modified_count:
        return {"message": "Item updated successfully"}
    else:
        return {"message": "Item not found"}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = collection.delete_one({"_id": item_id})
    if result.deleted_count:
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}
