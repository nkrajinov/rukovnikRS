from fastapi import FastAPI
from EditNote import router as edit_note_router

app = FastAPI()

# Uključivanje rutera za bilješke iz EditNote.py datoteke
app.include_router(edit_note_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
