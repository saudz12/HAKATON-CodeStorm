import json
import mongomock

# Creăm un client MongoDB "fake" în memorie
client = mongomock.MongoClient()

# Creăm baza de date existentă
db = client["myDatabase"]

# Creăm colecțiile deja existente
users_collection = db["users"]
courses_collection = db["courses"]
specializations_collection = db["specializations"]
lectures_collection = db["lectures"]
chat_prompts_collection = db["chatPrompts"]

# Creăm colecția pdfs doar dacă nu există deja
pdfs_collection = db.get_collection("pdfs")  # Dacă colecția există, o vom obține

# Dacă colecția nu există, o creăm
if not pdfs_collection:
    pdfs_collection = db["pdfs"]

# Inserăm un document de exemplu în colecția pdfs
pdf_document = {
    "pdfID": 1,
    "pdfTitle": "Introducere în Programare",
    "pdfPath": "/path/to/introducere_in_programare.pdf"
}
pdfs_collection.insert_one(pdf_document)

# Construim un dicționar care să conțină datele tuturor colecțiilor
database_dict = {}
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    documents = list(collection.find())
    # Conversie pentru câmpul _id (dacă există) în string
    for doc in documents:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    database_dict[collection_name] = documents

# Salvăm baza de date actualizată într-un fișier JSON
with open("databaseAPI.json", "w", encoding="utf-8") as f:
    json.dump(database_dict, f, ensure_ascii=False, indent=4)

print("Colecția 'pdfs' a fost adăugată la baza de date și salvată în 'database_dump.json'.")
