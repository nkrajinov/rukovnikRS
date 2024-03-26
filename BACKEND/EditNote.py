from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice)
collection = db["kartice"]

class Note(BaseModel):
    grad: str
    naziv_biljeske: str
    tekst: str
    user_id: Optional[str] = None  # Dodan user_id

@app.post("/notes/")
async def create_note(note: Note, user_id: str = Depends(get_current_user)):
    try:
        # Dodajte user_id u bilješku prije nego što je spremite
        note.user_id = user_id
        result = collection.insert_one(note.dict())
        return {"message": "Note created successfully", "note_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/{note_id}")
async def read_note(note_id: str):
    try:
        note = collection.find_one({"_id": note_id})
        if note:
            return note
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notes/{note_id}")
async def update_note(note_id: str, note: Note):
    try:
        result = collection.replace_one({"_id": note_id}, note.dict())
        if result.modified_count:
            return {"message": "Note updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/notes/{note_id}")
async def update_note_partial(note_id: str, updated_note: dict):
    try:
        result = collection.update_one({"_id": note_id}, {"$set": updated_note})
        if result.modified_count:
            return {"message": "Note updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    try:
        result = collection.delete_one({"_id": note_id})
        if result.deleted_count:
            return {"message": "Note deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dodajemo endpoint za čitanje svih bilješki za trenutnog korisnika
@app.get("/user/notes/")
async def read_user_notes(user_id: str = Depends(get_current_user)):
    try:
        notes = collection.find({"user_id": user_id})  # Filtriramo bilješke prema korisničkom identifikatoru
        return list(notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
