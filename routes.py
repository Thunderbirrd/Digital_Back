from app import app
from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
import json


@app.route('/register', methods=['POST'])
def register():
    if request.form:
        login = request.form.get("login")
        password = request.form.get("password")
        name = request.form.get("name")
        surname = request.form.get("surname")
        lastname = request.form.get("lastname")
        if User.check_login_is_unique(login):
            user = User(login, generate_password_hash(password), name, surname, lastname)
            user.save()
            return f"New user with login {user.login}"
        else:
            return "Такой логин уже занят"


@app.route('/login', methods=['POST'])
def login():
    if request.form:
        login = request.form.get("login")
        password = request.form.get("password")
        user = User.get_user_by_login(login)
        if user and check_password_hash(user.password, password):
            session["auth"] = user.id
            d = {
                "id": user.id,
                "login": user.login,
                "name": user.name,
                "surname": user.surname,
                "lastname": user.lastname
            }
            return json.dumps(d)
        else:
            return "Wrong login and/or password"


@app.route('/', methods=['GET'])
def index():
    return "Hello, world"
