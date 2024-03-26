from fastapi import HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["users"]

# Model za prijavu
class UserLogin(BaseModel):
    username: str
    password: str

# Endpoint za prijavu
async def login(user: UserLogin):
    user_data = users_collection.find_one({"username": user.username})
    if user_data and user_data["password"] == user.password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
