from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Ovo omogućuje CORS zahtjeve s bilo kojeg izvora (možete prilagoditi postavke prema potrebi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model za prijavu
class UserLogin(BaseModel):
    username: str
    password: str

# Simulacija baze podataka
fake_db = {}

# Endpoint za prijavu
@app.post("/login")
async def login(user: UserLogin):
    # Ovdje bi se obavila provjera korisničkih podataka u vašoj bazi podataka
    # Na primjer, možete provjeriti korisničko ime i lozinku u MongoDB bazi
    # Za ovaj primjer koristimo samo simulirani skup podataka
    if user.username in fake_db and fake_db[user.username] == user.password:
        return JSONResponse(content={"message": "Login successful"})
    else:
        return JSONResponse(status_code=401, content={"message": "Invalid username or password"})

# Endpoint za registraciju
@app.post("/signup")
async def signup(user: UserLogin):
    # Ovdje bi se obavila logika za registraciju korisnika
    # Na primjer, možete dodati novog korisnika u MongoDB bazu
    # Za ovaj primjer koristimo samo simulirani skup podataka
    fake_db[user.username] = user.password
    return JSONResponse(content={"message": "Signup successful"})

# Endpoint za homeview stranicu
@app.get("/home")
async def home():
    return {"message": "Welcome to the homeview page!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)