from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class Note(BaseModel):
    grad: str
    naziv_biljeske: str
    tekst: str