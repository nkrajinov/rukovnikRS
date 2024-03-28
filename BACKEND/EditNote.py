from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user
from bson import ObjectId  # Dodali smo uvoz za pretvaranje stringa u ObjectId

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
        result = collection.insert_one(note.model_dump())  # Zamijenjeno note.dict() s note.model_dump()
        return {"message": "Note created successfully", "note_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/{note_id}")
async def read_note(note_id: str):
    try:
        # Pretvorite note_id u ObjectId jer MongoDB koristi ObjectId za _id polje
        object_id = ObjectId(note_id)
        note = collection.find_one({"_id": object_id})
        if note:
            return note
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notes/{note_id}")
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

@app.patch("/notes/{note_id}")
async def update_note_partial(note_id: str, updated_note: dict):
    try:
        result = collection.update_one({"_id": ObjectId(note_id)}, {"$set": updated_note})
        if result.modified_count:
            return {"message": "Note updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/notes/{note_id}")
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
@app.get("/user/notes/")
async def read_user_notes(user_id: str = Depends(get_current_user)):
    try:
        notes = collection.find({"user_id": user_id})  # Filtriramo bilješke prema korisničkom identifikatoru
        return list(notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)