import json
import mongomock

# Creăm un client MongoDB "fake" în memorie
client = mongomock.MongoClient()

# Creăm baza de date
db = client["myDatabase"]

# Creăm colecțiile
users_collection = db["users"]
courses_collection = db["courses"]
specializations_collection = db["specializations"]
lectures_collection = db["lectures"]
chat_prompts_collection = db["chatPrompts"]

# Inserăm documente de exemplu în fiecare colecție

# Colecția users: userID, username, password
user_document = {
    "userID": 1,
    "username": "john_doe",
    "password": "secret123"
}
users_collection.insert_one(user_document)

# Colecția courses: courseID, courseName, specializationID
course_document = {
    "courseID": 101,
    "courseName": "Introducere în Matematică",
    "specializationID": 201
}
courses_collection.insert_one(course_document)

# Colecția specializations: specializationID, specializationName
specialization_document = {
    "specializationID": 201,
    "specializationName": "Științe exacte"
}
specializations_collection.insert_one(specialization_document)

# Colecția lectures: lectureName
lecture_document = {
    "lectureName": "Noțiuni de bază în algebra"
}
lectures_collection.insert_one(lecture_document)

# Colecția chatPrompts: chat
chat_prompt_document = {
    "chat": "Bună ziua, cum te pot ajuta astăzi?"
}
chat_prompts_collection.insert_one(chat_prompt_document)

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

# Salvăm baza de date (datele) într-un fișier JSON
with open("database_dump.json", "w", encoding="utf-8") as f:
    json.dump(database_dict, f, ensure_ascii=False, indent=4)

print("Baza de date a fost generată și salvată în 'database_dump.json'.")
