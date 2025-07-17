from src import app, db
from bcrypt import hashpw, gensalt
from src.models.user import User
from flask import request, jsonify

@app.route("/login", methods=["POST"])
def login():
    pass

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
def get_user():
    pass

@app.route("/logout", methods=["GET"])
def logout():
    pass