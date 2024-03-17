import pymongo

# Povezivanje s MongoDB serverom
# Zamijenite "mongodb://localhost:27017/" sa svojim URL-om dobivenim iz MongoDB Compassa
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice)
collection = db["ime_vase_kolekcije"]
print("database.py je uspješno izvršena.")