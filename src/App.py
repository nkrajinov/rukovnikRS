from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["users"]

# Definiranje modela za prijavu
class UserLogin(BaseModel):
    username: str
    password: str

# Definiranje rutera za signup
signup_router = APIRouter()

@signup_router.post("/signup")
async def signup(user: UserLogin):
    # Provjerite je li korisničko ime već zauzeto
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Korisničko ime već postoji")
    
    # Spremite korisnika u bazu podataka
    users_collection.insert_one(user.dict())
    
    return {"message": "Uspješna registracija"}

# Uključivanje rutera za signup u glavni router
app.include_router(signup_router)

# Omogućavanje CORS-a
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint za homeview stranicu
@app.get("/home")
async def home():
    return {"message": "Welcome to the homeview page!"}

# Import za autentifikaciju
from auth import login

# Endpoint za prijavu
@app.post("/login")
async def login_endpoint(user: UserLogin):
    return await login(user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
