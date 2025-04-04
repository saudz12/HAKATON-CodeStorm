from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  # Permite cereri din orice origine

# Conectare la MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

# Definirea colecțiilor
users_collection = db["users"]
courses_collection = db["courses"]
course_classes_collection = db["courseClasses"]
chat_prompts_collection = db["chatPrompts"]

# Ruta pentru înregistrare utilizator
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    if not username or not password:
        return jsonify({"status": "error", "message": "Username și parolă sunt necesare."}), 400

    # Verifică dacă utilizatorul există deja
    if users_collection.find_one({"username": username}):
        return jsonify({"status": "error", "message": "Utilizatorul există deja."}), 400

    user = {"username": username, "password": password}  # Parola în clar, doar pentru testare
    result = users_collection.insert_one(user)
    return jsonify({"status": "success", "message": "Utilizator înregistrat.", "user_id": str(result.inserted_id)})

# Ruta pentru login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "Username și parolă sunt necesare."}), 400

    user = users_collection.find_one({"username": username})
    if user and user.get("password") == password:
        return jsonify({"status": "success", "message": "Autentificare reușită.", "user": {"username": username}})
    else:
        return jsonify({"status": "error", "message": "Credentiale invalide."}), 401

# Ruta pentru preluarea detaliilor unui utilizator
@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"status": "error", "message": "Username-ul este necesar."}), 400

    user = users_collection.find_one({"username": username}, {"password": 0})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify({"status": "success", "user": user})
    else:
        return jsonify({"status": "error", "message": "Utilizatorul nu a fost găsit."}), 404

# Ruta pentru obținerea tuturor cursurilor
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = list(courses_collection.find())
    for course in courses:
        course["_id"] = str(course["_id"])
    return jsonify({"status": "success", "courses": courses})

# Ruta GET pentru obținerea unui curs specific (după nume și disciplină)
@app.route('/course', methods=['GET'])
def get_course():
    nume = request.args.get("nume", "").strip()
    disciplina = request.args.get("disciplina", "").strip()
    if not nume or not disciplina:
        return jsonify({"status": "error", "message": "Parametrii 'nume' și 'disciplina' sunt necesari."}), 400

    course = courses_collection.find_one({"nume": nume, "disciplina": disciplina})
    if course:
        course["_id"] = str(course["_id"])
        return jsonify({"status": "success", "course": course})
    else:
        return jsonify({"status": "error", "message": "Cursul nu a fost găsit."}), 404

# Ruta POST pentru adăugarea unui nou curs
@app.route('/course', methods=['POST'])
def post_course():
    data = request.get_json() or {}
    nume = data.get("nume", "").strip()
    disciplina = data.get("disciplina", "").strip()
    if not nume or not disciplina:
        return jsonify({"status": "error", "message": "Parametrii 'nume' și 'disciplina' sunt necesari."}), 400

    course = {
        "nume": nume,
        "disciplina": disciplina,
        "description": data.get("description", "")
    }
    result = courses_collection.insert_one(course)
    return jsonify({"status": "success", "message": "Curs adăugat.", "course_id": str(result.inserted_id)})

# Ruta pentru obținerea claselor de cursuri (courseClasses)
@app.route('/courseClasses', methods=['GET'])
def get_course_classes():
    classes = list(course_classes_collection.find())
    for c in classes:
        c["_id"] = str(c["_id"])
    return jsonify({"status": "success", "courseClasses": classes})

# Ruta POST pentru inserarea unui chat prompt
@app.route('/chatPrompt', methods=['POST'])
def post_chat_prompt():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"status": "error", "message": "Textul este necesar."}), 400

    chat_prompt = {"text": text}
    result = chat_prompts_collection.insert_one(chat_prompt)
    return jsonify({"status": "success", "message": "Chat prompt adăugat.", "prompt_id": str(result.inserted_id)})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
