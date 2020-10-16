from database import db
from flask import session


class Model:
    errors = []

    def validate(self):
        self.errors = []
        return len(self.errors) == 0

    def save(self):
        if self.validate():
            if self.id is None:
                db.session.add(self)
            db.session.commit()
            return True
        else:
            return False


class User(db.Model, Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    lastname = db.Column(db.String())

    def __init__(self, login="", password="", name="", surname="", lastname=""):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.lastname = lastname
        self.save()

    def set_login(self, new_login):
        self.login = new_login
        self.save()

    def set_password(self, new_pass):
        self.password = new_pass
        self.save()

    @staticmethod
    def get_user_by_login(login):
        return db.session.query(User).filter(User.login == login).first()

    @staticmethod
    def get_current_user():
        id = session.get("auth")
        return db.session.query(User).filter(User.id == id).first()

    @staticmethod
    def is_authorised():
        return User.get_current_user() is not None

    @staticmethod
    def get_login_by_id(i):
        user = db.session.query(User).filter(User.id == i).first()
        return user.login

    @staticmethod
    def check_login_is_unique(login):
        return db.session.query(User.login).filter(User.login == login).first() is None

    @staticmethod
    def auth(login, password):
        return db.session.query(User).filter(User.login == login).filter(User.password == password).first()


class Tag(db.Model, Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name
        self.save()

    @staticmethod
    def check_name_is_unique(name):
        return db.session.query(Tag.name).filter(Tag.name == name).first() is None

    @staticmethod
    def get_tag_by_id(i):
        return db.session.query(Tag.id).filter(Tag.id == i).first()
