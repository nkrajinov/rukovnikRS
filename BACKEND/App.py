from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["korisnici"]

# Odabir kolekcije (tablice) za kartice
kartice_collection = db["kartice"]

# Omogućavanje CORS-a
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    username: str
    password: str

class Note(BaseModel):
    grad: str
    naziv_biljeske: str
    tekst: str

# Endpoint za homeview stranicu
@app.get("/home")
async def home():
    return {"message": "Welcome to the homeview page!"}

router = APIRouter()

@router.post("/signup")
async def signup(user: UserLogin):
    # Provjerite je li korisničko ime već zauzeto
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Korisničko ime već postoji")
    
    # Spremite korisnika u bazu podataka
    users_collection.insert_one(user.dict())
    
    return {"message": "Uspješna registracija"}

@router.post("/login")
async def login(user: UserLogin):
    # Implementacija funkcije za prijavu
    # Ovdje provjerite korisničko ime i lozinku u bazi podataka
    # Vratite odgovarajući odgovor na temelju rezultata provjere
    pass  # Dodajte implementaciju funkcije za prijavu

@app.post("/notes/")
def create_note(note: Note):
    result = kartice_collection.insert_one(note.dict())
    return {"message": "Note created successfully", "note_id": str(result.inserted_id)}

# Uključivanje rutera iz modula signup
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
