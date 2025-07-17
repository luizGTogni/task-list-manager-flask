from os import getenv
from src import app, db
from src.models.user import User
from bcrypt import hashpw, gensalt

with app.app_context():
    db.drop_all()
    db.create_all()
    password_hashed = hashpw(str.encode(getenv("PASSWORD_ADMIN")), gensalt())
    user = User(username="toogni", email="contato.togni@gmail.com", password=password_hashed, role="admin")
    db.session.add(user)
    db.session.commit()
    print("Database created")