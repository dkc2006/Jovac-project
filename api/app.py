from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from bson import ObjectId
from flask_cors import CORS  # Import CORS
from flask import request, jsonify
from functools import wraps
import jwt
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
app.config['SECRET_KEY'] = 'secret-key'

mongo = PyMongo(app)

class User:
    def __init__(self, name, email, password, firstname, lastname, phone, dob, gender, aboutme):
        self.name = name
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.dob = dob
        self.gender = gender
        self.aboutme = aboutme

    def save(self):
        mongo.db.users.insert_one({
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'phone': self.phone,
            'dob': self.dob,
            'gender': self.gender,
            'aboutme': self.aboutme
        })

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})


@app.route('/')
def index():
    return 'Welcome to The Camping Adventure App'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    try:
        user_data = User.find_by_email(email)

        if not user_data:
            return jsonify({'error': 'Invalid email or password'}), 401

        if not check_password_hash(user_data.get('password', ''), password):
            return jsonify({'error': 'Invalid email or password'}), 401

        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'user_id': str(user_data['_id']),
            'exp': expiration
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        user_data['_id'] = str(user_data['_id'])
        return jsonify({'token': token, 'user': user_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        existing_user = User.find_by_email(data.get('email'))
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone = data.get('phone')
        dob = data.get('dob')
        gender = data.get('gender')
        aboutme = data.get('aboutme')

        if len(firstname)<3:
            return jsonify({'error': 'Name should be at least 3 characters long'}), 400
        
        if not all([name, email, password, firstname, lastname, phone, dob, gender, aboutme]):
            return jsonify({'error': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password)
        user = User(name, email, hashed_password, firstname, lastname, phone, dob, gender, aboutme)
        user.save()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/register', methods=['GET'])
def render_register():
    return render_template('register.html')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            token = token.split(" ")[1]  # Extract token after "Bearer "
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'error': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    user_data = {
        "name": current_user['name'],
        "email": current_user['email']
    }
    return jsonify(user_data), 200


if __name__ == "__main__":
    app.run(debug=True)
