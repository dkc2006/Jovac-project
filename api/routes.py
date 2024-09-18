# from flask import Blueprint, render_template, request, jsonify, current_app
# from werkzeug.security import generate_password_hash, check_password_hash

# # Create a blueprint for authentication routes
# auth_routes = Blueprint('auth_routes', __name__)

# # Route for login
# @auth_routes.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         mongo = current_app.config['mongo']  # Access the mongo instance from app config
#         users = mongo.db.users  # 'users' is the collection in MongoDB

#         # Retrieve the user by email
#         login_user = users.find_one({'email': request.form['email']})

#         # Check if the user exists and verify the password
#         if login_user and check_password_hash(login_user['password'], request.form['password']):
#             return jsonify({'message': 'Login successful!'}), 200
#         return jsonify({'message': 'Invalid email or password'}), 401

#     return render_template('login.html')  # Return the login HTML page

# # Route for registration
# @auth_routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         mongo = current_app.config['mongo']  # Access the mongo instance from app config
#         users = mongo.db.users  # 'users' is the collection in MongoDB

#         # Check if the user already exists
#         existing_user = users.find_one({'email': request.form['email']})

#         if existing_user is None:
#             # Hash the password before storing it
#             hashpass = generate_password_hash(request.form['password'])

#             # Insert the user data into the database
#             users.insert_one({
#                 'email': request.form['email'],
#                 'password': hashpass,
#                 'firstname': request.form.get('firstname', ''),
#                 'lastname': request.form.get('lastname', ''),
#                 # Add additional fields here if needed (phone, dob, etc.)
#             })

#             return jsonify({'message': 'Registration successful!'}), 201
#         return jsonify({'message': 'Email already exists!'}), 400

#     return render_template('register.html')  # Return the register HTML page
