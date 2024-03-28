from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jwt import encode
from auth import JWT_SECRET_KEY, ALGORITHM, login, get_current_user, myctx  # Dodali smo myctx iz auth.py
from database import db, kartice_collection, users_collection
from models import Note, UserLogin

app = FastAPI()

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

router = APIRouter()

@router.post("/signup")
async def signup(user: UserLogin):
    # Provjerite je li korisničko ime već zauzeto
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Korisničko ime već postoji")
    
    # Hashirajte lozinku prije spremanja u bazu podataka
    hashed_password = myctx.hash(user.password)
    
    # Spremite korisnika u bazu podataka
    users_collection.insert_one({"username": user.username, "password": hashed_password})
    
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
    if not myctx.verify(user.password, user_data["password"]):  # Promijenili smo pwd_context u myctx
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generiraj JWT token
    token = encode({"sub": user.username}, JWT_SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes/")
def create_note(note: Note):
    result = kartice_collection.insert_one(note.model_dump())
    return {"message": "Note created successfully", "note_id": str(result.inserted_id)}

# Uključivanje rutera iz modula signup
app.include_router(router)

@app.get("/user/notes/")
async def read_user_notes(user: str = Depends(get_current_user)):
    notes = kartice_collection.find({"user_id": user})
    return list(notes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
