from fastapi import FastAPI, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from auth import login, get_current_user

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice) za bilješke
collection = db["kartice"]

class Note(BaseModel):
    grad: str
    naziv_biljeske: str
    tekst: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/user/notes/")
async def read_user_notes(user: str = Depends(get_current_user)):
    notes = collection.find({"user_id": user})
    return list(notes)

@app.get("/notes/{note_id}")
def read_note(note_id: str):
    note = collection.find_one({"_id": note_id})
    if note:
        return note
    else:
        return {"message": "Note not found"}

@app.post("/notes")
def create_note(note: Note):
    note_data = note.dict(by_alias=True, exclude_unset=True)
    result = collection.insert_one(note_data)
    return {"message": "Note created successfully", "note_id": str(result.inserted_id)}

@app.put("/notes/{note_id}")
def update_note(note_id: str, note: Note):
    result = collection.replace_one({"_id": note_id}, note.dict())
    if result.modified_count:
        return {"message": "Note updated successfully"}
    else:
        return {"message": "Note not found"}

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    result = collection.delete_one({"_id": note_id})
    if result.deleted_count:
        return {"message": "Note deleted successfully"}
    else:
        return {"message": "Note not found"}

# Endpoint za prijavu
@app.post("/login")
async def login_endpoint(user: dict):
    return await login(user)
