from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
from database import db, kartice_collection , users_collection
from jwt import encode
from auth import JWT_SECRET_KEY, ALGORITHM

app = FastAPI()

# Definicija konteksta lozinke
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

 # Implementacija funkcije za prijavu
@router.post("/login")
async def login(user: UserLogin):
   # Pronađi korisnika u bazi podataka prema korisničkom imenu
    user_data = users_collection.find_one({"username": user.username})
    
    # Provjeri postoji li korisnik s tim korisničkim imenom
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Provjeri odgovara li unesena lozinka lozinci spremljenoj u bazi podataka
    if not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generiraj JWT token
    token = encode({"sub": user.username}, JWT_SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes/")
def create_note(note: Note):
    result = kartice_collection.insert_one(note.dict())
    return {"message": "Note created successfully", "note_id": str(result.inserted_id)}

# Uključivanje rutera iz modula signup
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
