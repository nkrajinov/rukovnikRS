from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice)
collection = db["ime_vase_kolekcije"]

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
