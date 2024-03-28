from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel
from models import Note  # Dodano uvoz za model Note

app = FastAPI()

# Uspostavljanje veze s MongoDB serverom
client = MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice) za bilješke
collection = db["kartice"]

@app.get("/")
def read_root():
    return {"message": "Hello World"}

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

@app.patch("/notes/{note_id}")
def update_note_partial(note_id: str, updated_note: dict):
    result = collection.update_one({"_id": note_id}, {"$set": updated_note})
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
