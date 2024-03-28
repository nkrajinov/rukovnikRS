from fastapi import HTTPException, Depends
from jwt import PyJWTError, decode, encode
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from models import UserLogin
from database import users_collection

# Definicija algoritma i tajnog ključa
ALGORITHM = "HS256"
JWT_SECRET_KEY = "your_secret_key_here"

# Definicija algoritama za hashiranje lozinke
myctx = CryptContext(schemes=["sha256_crypt", "ldap_salted_md5"])

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funkcija za provjeru lozinke
async def login(user: UserLogin):
    user_data = users_collection.find_one({"username": user.username})
    if user_data and myctx.verify(user.password, user_data["password"]):
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
