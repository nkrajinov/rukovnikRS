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

# Endpoint za homeview stranicu
@app.get("/home")
async def home():
    return {"message": "Welcome to the homeview page!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)