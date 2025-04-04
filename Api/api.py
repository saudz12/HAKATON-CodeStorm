from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  # Permite cereri din orice origine

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["database"]
    print("Conexiune la MongoDB reușită!")
except Exception as e:
    print("Eroare la conectarea la MongoDB:", e)

# Definirea colecțiilor
users_collection = db["users"]             # Documente: { "userID": <int>, "username": <str>, "password": <str> }
courses_collection = db["courses"]           # Documente: { "courseID": <int>, "courseName": <str>, "specializationID": <int>, "description": <str> }
specializations_collection = db["specializations"]  # Documente: { "specializationID": <int>, "specializationName": <str> }
lectures_collection = db["lectures"]         # Documente: { "lectureName": <str> }
chat_prompts_collection = db["chatPrompts"]  # Documente: { "chat": <str> }

# ---------------------- Endpoint-uri pentru utilizatori ----------------------

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

    # Pentru identificare se poate folosi fie un ID generat automat, fie un userID definit
    user = {"username": username, "password": password}
    result = users_collection.insert_one(user)
    return jsonify({
        "status": "success",
        "message": "Utilizator înregistrat.",
        "user_id": str(result.inserted_id)
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "Username și parolă sunt necesare."}), 400

    user = users_collection.find_one({"username": username})
    if user and user.get("password") == password:
        return jsonify({
            "status": "success",
            "message": "Autentificare reușită.",
            "user": {"username": username}
        })
    else:
        return jsonify({"status": "error", "message": "Credentiale invalide."}), 401

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

# ---------------------- Endpoint-uri pentru cursuri ----------------------

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = list(courses_collection.find())
    for course in courses:
        course["_id"] = str(course["_id"])
    return jsonify({"status": "success", "courses": courses})

@app.route('/course', methods=['GET'])
def get_course():
    # Căutare după numele cursului; se poate extinde și cu filtrare după specializare
    course_name = request.args.get("courseName", "").strip()
    if not course_name:
        return jsonify({"status": "error", "message": "Parametrul 'courseName' este necesar."}), 400

    course = courses_collection.find_one({"courseName": course_name})
    if course:
        course["_id"] = str(course["_id"])
        return jsonify({"status": "success", "course": course})
    else:
        return jsonify({"status": "error", "message": "Cursul nu a fost găsit."}), 404

@app.route('/course', methods=['POST'])
def post_course():
    data = request.get_json() or {}
    course_id = data.get("courseID")
    course_name = data.get("courseName", "").strip()
    specialization_id = data.get("specializationID")
    
    if not course_id or not course_name or not specialization_id:
        return jsonify({
            "status": "error",
            "message": "Parametrii 'courseID', 'courseName' și 'specializationID' sunt necesari."
        }), 400

    course = {
        "courseID": course_id,
        "courseName": course_name,
        "specializationID": specialization_id,
        "description": data.get("description", "")
    }
    result = courses_collection.insert_one(course)
    return jsonify({
        "status": "success",
        "message": "Curs adăugat.",
        "course_id": str(result.inserted_id)
    })

# ---------------------- Endpoint-uri pentru specializări ----------------------

@app.route('/specializations', methods=['GET'])
def get_specializations():
    specs = list(specializations_collection.find())
    for spec in specs:
        spec["_id"] = str(spec["_id"])
    return jsonify({"status": "success", "specializations": specs})

@app.route('/specializations', methods=['POST'])
def post_specialization():
    data = request.get_json() or {}
    specialization_id = data.get("specializationID")
    specialization_name = data.get("specializationName", "").strip()
    if not specialization_id or not specialization_name:
        return jsonify({
            "status": "error",
            "message": "Parametrii 'specializationID' și 'specializationName' sunt necesari."
        }), 400

    specialization = {
        "specializationID": specialization_id,
        "specializationName": specialization_name
    }
    result = specializations_collection.insert_one(specialization)
    return jsonify({
        "status": "success",
        "message": "Specializare adăugată.",
        "specialization_id": str(result.inserted_id)
    })

# ---------------------- Endpoint-uri pentru prelegeri ----------------------

@app.route('/lectures', methods=['GET'])
def get_lectures():
    lectures = list(lectures_collection.find())
    for lecture in lectures:
        lecture["_id"] = str(lecture["_id"])
    return jsonify({"status": "success", "lectures": lectures})

@app.route('/lectures', methods=['POST'])
def post_lecture():
    data = request.get_json() or {}
    lecture_name = data.get("lectureName", "").strip()
    if not lecture_name:
        return jsonify({
            "status": "error",
            "message": "Parametrul 'lectureName' este necesar."
        }), 400

    lecture = {"lectureName": lecture_name}
    result = lectures_collection.insert_one(lecture)
    return jsonify({
        "status": "success",
        "message": "Lectură adăugată.",
        "lecture_id": str(result.inserted_id)
    })

# ---------------------- Endpoint pentru chat prompts ----------------------

@app.route('/sample-page', methods=['POST'])
def post_chat_prompt():
    try:
        print("✅ Request primit")
        data = request.get_json(force=True)  # force = încearcă să decodeze chiar dacă headerul e greșit
        print("=== JSON PRIMIT ===", data)

        chat_text = data.get("chat") if data else None
        if not isinstance(chat_text, str) or not chat_text.strip():
            return jsonify({"status": "error", "message": "Textul este necesar."}), 400

        chat_prompt = {"chat": chat_text.strip()}
        print("=== Prompt de inserat ===", chat_prompt)

        result = chat_prompts_collection.insert_one(chat_prompt)

        return jsonify({
            "status": "success",
            "message": "Chat prompt adăugat.",
            "prompt_id": str(result.inserted_id)
        })
    except Exception as e:
        print("❌ Eroare:", e)
        return jsonify({"status": "error", "message": f"Eroare la salvare: {str(e)}"}), 500



if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, host='127.0.0.1', port=5000)

