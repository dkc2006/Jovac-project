import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory 
from flask_pymongo import PyMongo
from db import mdb
from werkzeug.security import generate_password_hash, check_password_hash

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create the Flask app with the correct template folder
app = Flask(__name__, template_folder=parent_dir)

# Configure static files to be served from the parent directory
app.static_folder = parent_dir

# app.config["MONGO_URI"] = "mongodb://localhost:27017/"

mongo = PyMongo(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                return jsonify({'message': 'Login successful!'}), 200
        return jsonify({'message': 'Invalid email or password'}), 401

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        existing_user = mdb.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            mdb.insert_one({
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],
                # 'email': request.form['email'],
                # 'password': hashpass,
                # 'phone': request.form['phone'],
                # 'dob': request.form['dob'],
                # 'gender': request.form['gender'],
                # 'hobbies': request.form.getlist('hobbies'),
                # 'address': {
                #     'housenumber': request.form['housenumber'],
                #     'street': request.form['street'],
                #     'city': request.form['city'],
                #     'state': request.form['state'],
                #     'country': request.form['country'],
                #     'pincode': request.form['pincode']
                # },
                # 'aboutme': request.form['aboutme']
            })
            return jsonify({'message': 'Registration successful!'}), 201
        return jsonify({'message': 'Email already exists!'}), 400

    return render_template('register.html')

@app.route('/booking', methods=['GET'])
def booking():
    return render_template('booking.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)