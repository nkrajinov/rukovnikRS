from pymongo import MongoClient
import pymongo
from models import Note  # Dodano uvoz za model Note

# Povezivanje s MongoDB serverom
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["rukovnikbaza"]

# Odabir kolekcije (tablice) za korisnike
users_collection = db["korisnici"]

# Odabir kolekcije (tablice) za kartice
kartice_collection = db["kartice"]

print("database.py je uspješno izvršena.")