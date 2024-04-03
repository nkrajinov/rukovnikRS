from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user
from bson import ObjectId  # Dodali smo uvoz za pretvaranje stringa u ObjectId
from bson.json_util import dumps
from models import Note

router = APIRouter()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice)
collection = db["kartice"]

@router.post("/notes/")
async def create_note(note: Note, user_id: str = Depends(get_current_user)):
    try:
        # Dodajte user_id u bilješku prije nego što je spremite
        note.user_id = user_id
        # Uklonite _id iz rezultata koji se sprema u bazu
        note_dict = note.dict()
        note_dict.pop("_id", None)
        result = collection.insert_one(note_dict)
        return {"message": "Note created successfully", "note_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")

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
        result = collection.replace_one({"_id": object_id}, note.dict(by_alias=True))
        
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

@router.get("/user/notes/")
async def read_user_notes(user_id: str = Depends(get_current_user)):
    try:
        # Dobij sve bilješke korisnika iz baze podataka
        notes = collection.find({"user_id": user_id})

        # Konvertiraj rezultate u listu Python rječnika, izbacujući "_id" polje
        notes_list = []
        for note in notes:
            note_dict = dict(note)
            note_dict.pop("_id", None)
            notes_list.append(note_dict)

        # Vrati listu bilješki korisnika
        return notes_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read user notes: {str(e)}")
@router.post("/notes/search/")
async def search_notes(keyword: str):
    try:
        # Pretraži sve bilješke koje sadrže ključni pojam u poljima "grad", "naziv_biljeske" i "tekst"
        search_results = collection.find({
            "$or": [
                {"grad": {"$regex": keyword, "$options": "i"}},
                {"naziv_biljeske": {"$regex": keyword, "$options": "i"}},
                {"tekst": {"$regex": keyword, "$options": "i"}}
            ]
        })

        # Konvertiraj rezultate u listu Python rječnika, izbacujući "_id" polje
        search_results_list = []
        for note in search_results:
            note_dict = dict(note)
            note_dict.pop("_id", None)
            search_results_list.append(note_dict)

        # Vrati rezultate pretrage
        return search_results_list
    except Exception as e:
        error_message = f"Failed to search notes: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)