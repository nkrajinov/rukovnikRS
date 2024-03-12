import pymongo

# Uspostavljanje veze s MongoDB serverom
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Odabir baze podataka
db = client["ime_vase_baze"]

# Odabir kolekcije (tablice)
collection = db["ime_vase_kolekcije"]