from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.agent import AiResponse

app = Flask(__name__)
CORS(app)  # Permite cereri din orice origine

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asigurăm că folderul există
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ai = AiResponse(api_key='key')

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["databaseAPI"]
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

@app.route('/dashboard/default/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    firstName = data.get("firstName","").strip()
    lastName = data.get("lastName","").strip()
    company = data.get("company","").strip()
    userType = data.get("userType","").strip()

    if not email or not password:
        return jsonify({"status": "error", "message": "Email și parolă sunt necesare."}), 400

    # Verifică dacă utilizatorul există deja
    if users_collection.find_one({"email": email}):
        return jsonify({"status": "error", "message": "Utilizatorul există deja."}), 400

    # Pentru identificare se poate folosi fie un ID generat automat, fie un userID definit
    user = {"email": email, "password": password,"company":company, "firstName": firstName, "lastName": lastName , "userType": userType}
    result = users_collection.insert_one(user)
    return jsonify({
        "status": "success",
        "message": "Utilizator înregistrat.",
        "user_id": str(result.inserted_id)
    })

@app.route('/dashboard/default/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not email or not password:
        return jsonify({"status": "error", "message": "Email și parolă sunt necesare."}), 400

    user = users_collection.find_one({"email": email})

    if user and user.get("password") == password:
        return jsonify({
            "status": "success",
            "message": "Autentificare reușită.",
            "user": {"email": email}
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

@app.route('/dashboard/courses', methods=['GET'])
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
        "specializationID": 0,
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

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        # 1. Verificăm dacă cererea conține fișierul PDF
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "Fișierul nu a fost trimis."}), 400

        file = request.files['file']

        # 2. Verificăm dacă fișierul are extensia corectă
        if file.filename == '':
            return jsonify({"status": "error", "message": "Numele fișierului este gol."}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "Fișierul nu este un PDF valid."}), 400

        # 3. Salvăm fișierul pe server (sau îl procesăm dacă e necesar)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # 4. Poți adăuga orice procesare a fișierului PDF aici (de exemplu, extragerea de text, etc.)

        # 5. Răspuns JSON cu mesaj
        return jsonify({"status": "success", "message": "Fișierul PDF a fost încărcat cu succes."}), 200

    except Exception as e:
        # 6. Gestionarea erorilor
        return jsonify({"status": "error", "message": f"Eroare la procesarea fișierului: {str(e)}"}), 500

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
        data = request.get_json(force=True)
        print("=== JSON PRIMIT ===", data)

        chat_text = data.get("chat") if data else None
        
        if not isinstance(chat_text, str) or not chat_text.strip():
            return jsonify({"status": "error", "message": "Textul este necesar."}), 400
        
        chat_text = chat_text.strip()
        print("=== Text preprocesat ===", chat_text)

        ai_response = ai.ask_question(chat_text)

        if not ai_response:
            return jsonify({"status": "error", "message": "Răspuns invalid de la AI."}), 500

        print("=== Răspuns AI ===", ai_response)

        chat_prompt = {
            "chat": chat_text,
            "ai_response": ai_response
        }

        result = chat_prompts_collection.insert_one(chat_prompt)
        inserted_id = str(result.inserted_id)

        return jsonify({
            "status": "success",
            "message": "Chat prompt adăugat și procesat de AI.",
            "prompt_id": inserted_id,
            "ai_response": ai_response
        })

    except Exception as e:
        print("❌ Eroare:", e)
        return jsonify({"status": "error", "message": f"Eroare la salvare: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

