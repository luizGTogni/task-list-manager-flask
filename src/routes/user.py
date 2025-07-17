from src import app, db
from bcrypt import hashpw, gensalt, checkpw
from src.models.user import User
from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    if username and password:
        user_attempted = User.query.filter_by(username=username).first()

        if user_attempted:
            if checkpw(str.encode(password), user_attempted.password):
                login_user(user_attempted)
                return jsonify({ "message": "Login successfully", "user_id": user_attempted.id }), 200
        
        return jsonify({ "error": "Credentials invalid" }), 401

    return jsonify({ "error": "Credentials is missing or invalid" }), 400

@app.route("/users", methods=["POST"])
def create_user():
    body = request.get_json()
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")

    if username and email and password:
        user = User.query.filter_by(username=username).first()
        
        if user:
            return jsonify({ "error": "Username already exists" }), 409
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            return jsonify({ "error": "Email already exists" }), 409

        password_hashed = hashpw(str.encode(password), gensalt())
        new_user = User(username=username, email=email, password=password_hashed)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({ "message": "User created successfully", "user_id": new_user.id }), 201

    return jsonify({ "error": "Credentials is missing or invalid" }), 400

@app.route("/users/me", methods=["GET"])
@login_required
def get_user():
    pass

@app.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({ "message": "Logout successfully" })
    
    return jsonify({ "error": "You do not have permission for this operation" }), 401