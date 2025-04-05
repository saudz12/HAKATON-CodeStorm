import json
from pymongo import MongoClient

# Conectare la MongoDB local
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["databaseAPI"]
    print("Conexiune la MongoDB reușită!")
except Exception as e:
    print("Eroare la conectarea la MongoDB:", e)

# Definirea colecțiilor existente
users_collection = db["users"]
courses_collection = db["courses"]
specializations_collection = db["specializations"]
lectures_collection = db["lectures"]
chat_prompts_collection = db["chatPrompts"]

# Lista de PDF-uri pentru fiecare curs, în funcție de domeniu
courses_with_pdfs = {
    101: {  # Cursul de matematică (Matematica)
        "courseName": "Matematica",
        "pdfs": [
            {"pdfTitle": "Algebra", "pdfPath": "./pdfs/Algebra.pdf"},
            {"pdfTitle": "Geometry", "pdfPath": "./pdfs/Geometry.pdf"}
        ]
    },
    102: {  # Cursul de informatică
        "courseName": "Informatica",
        "pdfs": [
            {"pdfTitle": "Data structures", "pdfPath": "./pdfs/DataStructure.pdf"},
            {"pdfTitle": "Sorting algorithms", "pdfPath": "./pdfs/Structure.pdf"}
        ]
    }
}

# Inserăm un document exemplu în colecția "users"
user_document = {
    "userID": 1,
    "firstName": "Andrei",
    "lastName": "Arustei",
    "company": "UNITBV",
    "email": "andrei@gmail.com",
    "password": "secret123"
}
users_collection.insert_one(user_document)

# Inserăm documente pentru cursuri, cu PDF-uri
for course_id, course_data in courses_with_pdfs.items():
    course_document = {
        "courseID": course_id,
        "courseName": course_data["courseName"],
        "specializationID": 201  # Exemplu: asociem cursul cu o specializare
    }
    
    # Inserăm cursul în colecția "courses"
    courses_collection.insert_one(course_document)
    
    # Actualizăm cursul cu PDF-urile asociate
    courses_collection.update_one(
        {"courseID": course_id},  # Căutăm cursul după ID
        {"$set": {"pdfs": course_data["pdfs"]}}   # Setăm PDF-urile pentru curs
    )

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

print("Baza de date a fost actualizată cu PDF-uri pentru fiecare curs și salvată în 'databaseAPI.json'.")
