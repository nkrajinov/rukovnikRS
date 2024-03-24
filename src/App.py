from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from Signup import signup

app = FastAPI()

# Uključivanje rutera iz modula signup
app.include_router(signup.router)

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
from auth import login, UserLogin

# Endpoint za prijavu
@app.post("/login")
async def login_endpoint(user: UserLogin):
    return await login(user)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)