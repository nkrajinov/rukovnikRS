from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user
from bson import ObjectId  # Dodali smo uvoz za pretvaranje stringa u ObjectId
from bson.json_util import dumps

router = APIRouter()

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

@router.post("/notes/")
async def create_note(note: Note, user_id: str = Depends(get_current_user)):
    try:
        # Dodajte user_id u bilješku prije nego što je spremite
        note.user_id = user_id
        # Uklonite _id iz rezultata koji se sprema u bazu
        note_dict = note.model_dump()
        note_dict.pop("_id", None)
        result = collection.insert_one(note_dict)
        return {"message": "Note created successfully", "note_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notes/{note_id}")
async def read_note(note_id: str):
    try:
        # Pretvorite note_id u ObjectId jer MongoDB koristi ObjectId za _id polje
        object_id = ObjectId(note_id)
        # Uklonite _id iz rezultata koji se dohvaća iz baze
        note = collection.find_one({"_id": object_id}, {"_id": 0})
        if note:
            return note
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/notes/{note_id}")
async def update_note(note_id: str, note: Note):
    try:
        # Pretvorite note_id u ObjectId jer MongoDB koristi ObjectId za _id polje
        object_id = ObjectId(note_id)
        
        # Koristite replace_one metodu kako biste zamijenili postojeći dokument s novim
        result = collection.replace_one({"_id": object_id}, note.model_dump(by_alias=True))  # Zamijenjeno note.dict() s note.model_dump()
        
        # Provjerite je li dokument uspješno ažuriran
        if result.modified_count:
            return {"message": "Note updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/notes/{note_id}")
async def update_note_partial(note_id: str, updated_note: dict):
    try:
        result = collection.update_one({"_id": ObjectId(note_id)}, {"$set": updated_note})
        if result.modified_count:
            return {"message": "Note updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(note_id)})
        if result.deleted_count:
            return {"message": "Note deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dodajemo endpoint za čitanje svih bilješki za trenutnog korisnika
@router.get("/user/notes/")
async def read_user_notes(user_id: str = Depends(get_current_user)):
    try:
        notes = collection.find({"user_id": user_id})  # Filtriramo bilješke prema korisničkom identifikatoru
        # Konvertiramo rezultate u listu Python rječnika
        notes_list = [dict(note) for note in notes]  # Pretvaranje objekata u rječnike
        # Vraćamo konvertiranu listu bilješki
        return notes_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))