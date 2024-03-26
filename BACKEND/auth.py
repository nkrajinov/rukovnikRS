from fastapi import HTTPException , Depends
from pymongo import MongoClient
from pydantic import BaseModel
from jwt import PyJWTError, decode, encode
from typing import Optional
from passlib.context import CryptContext
from auth import JWT_SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["korisnici"]

# Model za prijavu
class UserLogin(BaseModel):
    username: str
    password: str

# Funkcija za provjeru lozinke
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funkcija za prijavu korisnika
async def login(user: UserLogin):
    user_data = users_collection.find_one({"username": user.username})
    if user_data and pwd_context.verify(user.password, user_data["password"]):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Funkcija za dohvaćanje trenutnog korisnika iz autentifikacijskog tokena
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
