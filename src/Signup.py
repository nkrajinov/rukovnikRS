from collections import UserDict
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from auth import UserLogin

router = APIRouter()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["users"]

@router.post("/signup")
async def signup(user: UserLogin):
    # Provjerite je li korisničko ime već zauzeto
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Korisničko ime već postoji")
    
    # Spremite korisnika u bazu podataka
    users_collection.insert_one(user.dict())
    
    return {"message": "Uspješna registracija"}

@router.post("/login")
async def login(user: UserDict):
    # Implementacija funkcije za prijavu
    # Ovdje provjerite korisničko ime i lozinku u bazi podataka
    # Vratite odgovarajući odgovor na temelju rezultata provjere
    pass  # Dodajte implementaciju funkcije za prijavu