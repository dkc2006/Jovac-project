from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from flask_cors import CORS
import jwt
import requests
from functools import wraps

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
app.config['SECRET_KEY'] = 'secret-key'
WEATHER_API_KEY = 'b7b707f4b456ed3c8ed3559f68837809'

mongo = PyMongo(app)

# User Model
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


# Token Decorator
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


# Routes
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
        if not user_data or not check_password_hash(user_data.get('password', ''), password):
            return jsonify({'error': 'Invalid email or password'}), 401

        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {'user_id': str(user_data['_id']), 'exp': expiration}
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

        if len(firstname) < 3:
            return jsonify({'error': 'Name should be at least 3 characters long'}), 400
        if not all([name, email, password, firstname, lastname, phone, dob, gender, aboutme]):
            return jsonify({'error': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password)
        user = User(name, email, hashed_password, firstname, lastname, phone, dob, gender, aboutme)
        user.save()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    user_data = {"name": current_user['name'], "email": current_user['email']}
    return jsonify(user_data), 200


@app.route('/weather-report', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed']
                }
                return jsonify(weather_data)
            else:
                return jsonify({'error': 'City not found or invalid API request.'}), 400
        except Exception as e:
            return jsonify({'error': f'Error fetching data: {str(e)}'}), 500
    else:
        return jsonify({'error': 'City parameter is missing.'}), 400


@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    try:
        data = request.get_json()
        rating = data.get('rating')
        user_id = data.get('user_id')
        if not rating or not (1 <= int(rating) <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        mongo.db.ratings.insert_one({
            'user_id': user_id,
            'rating': int(rating),
            'submitted_at': datetime.utcnow()
        })

        return jsonify({'message': 'Thank you for your rating!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
