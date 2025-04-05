import json
import mongomock

# Creăm un client MongoDB "fake" în memorie
client = mongomock.MongoClient()

# Creăm baza de date existentă
db = client["databaseAPI"]

# Creăm colecțiile deja existente
users_collection = db["users"]
courses_collection = db["courses"]
specializations_collection = db["specializations"]
lectures_collection = db["lectures"]
chat_prompts_collection = db["chatPrompts"]

# Lista de lecții și PDF-uri pentru fiecare curs
courses_with_lectures_and_pdfs = {
    101: [  # Cursul cu ID-ul 101
        {
            "lectureName": "Matematica",
            "pdfs": [
                {"pdfTitle": "Algebra", "pdfPath": "./pdfs/algebra.pdf"},
                {"pdfTitle": "Complex numbers", "pdfPath": "./pdfs/ComplexNumbers.pdf"}
            ]
        },
        {
            "lectureName": "Informatica",
            "pdfs": [
                {"pdfTitle": "Data Structures", "pdfPath": "./pdfs/DataStructure.pdf"},
                {"pdfTitle": "Sorting", "pdfPath": "./pdfs/Sorting.pdf"},
            ]
        }
    ]
}

# Inserăm documente de exemplu în colecțiile existente (aceasta este aceeași logică ca înainte)
user_document = {
    "userID": 1,
    "firstName" : "Andrei",
    "lastName" : "Arustei",
    "company" : "UNITBV",
    "email": "andrei@gmail.com",
    "password": "secret123"
}
users_collection.insert_one(user_document)

course_document = {
    "courseID": 101,
    "courseName": "Introducere în Matematică",
    "specializationID": 201
}
courses_collection.insert_one(course_document)

# Adăugăm lecțiile și PDF-urile pentru fiecare curs
for course_id, lectures in courses_with_lectures_and_pdfs.items():
    # Găsim cursul pe baza ID-ului
    course = courses_collection.find_one({"courseID": course_id})
    
    if course:
        # Dacă cursul există, adăugăm sau actualizăm lecțiile și PDF-urile asociate
        courses_collection.update_one(
            {"courseID": course_id},  # Căutăm cursul după ID
            {"$set": {"lectures": lectures}}   # Setăm lecțiile și PDF-urile pentru curs
        )
    else:
        print(f"Cursul cu ID-ul {course_id} nu a fost găsit.")

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

print("Baza de date a fost actualizată cu lecții și PDF-uri pentru fiecare curs și salvată în 'database_dump.json'.")
