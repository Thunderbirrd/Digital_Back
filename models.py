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
    def get_login_by_id(i):
        user = db.session.query(User).filter(User.id == i).first()
        return user.login

    @staticmethod
    def check_login_is_unique(login):
        return db.session.query(User.login).filter(User.login == login).first() is None


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


class TaskTable(db.Model, Model):
    __tablename__ = 'task_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    admin = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, admin_id):
        self.name = name
        self.admin = admin_id
        self.save()

    @staticmethod
    def check_name_is_unique(name):
        return db.session.query(TaskTable.name).filter(TaskTable.name == name).first() is None


class Task(db.Model, Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    short_desc = db.Column(db.String())
    leader = db.Column(db.Integer, db.ForeignKey(User.id))
    parent = db.Column(db.Integer, db.ForeignKey(id))
    executor = db.Column(db.Integer, db.ForeignKey(User.id))
    taskboard_id = db.Column(db.Integer, db.ForeignKey(TaskTable.id))
    intensity = db.Column(db.Integer)

    @staticmethod
    def get_task_by_id(i):
        return db.session.query(Task.id).filter(Task.id == i).first()

    @staticmethod
    def get_task_by_executor_id(i):
        return db.session.query(Task.executor).filter(Task.executor == i).first()


class TaskTag(db.Model, Model):
    __tablename__ = 'task_tag'
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey(Task.id), nullable=False)
    id_tag = db.Column(db.Integer, db.ForeignKey(Tag.id), nullable=False)

    def __init__(self, task, tag):
        self.id_task = task
        self.id_tag = tag
        self.save()

    @staticmethod
    def get_all_tasks_by_tag(tag_id):
        manytomany = db.session.query(TaskTag.id_tag).filter(TaskTag.id_tag == tag_id).all()
        tasks_id = []
        for t in manytomany:
            tasks_id.append(t.id_task)
        tasks = []
        for t in tasks_id:
            tasks.append(Task.get_task_by_id(t))
        return tasks

    @staticmethod
    def get_all_tasks_tags(task_id):
        manytomany = db.session.query(TaskTag.id_task).filter(TaskTag.id_task == task_id).all()
        tag_id = []
        for t in manytomany:
            tag_id.append(t.id_tag)
        tags = []
        for t in tag_id:
            tags.append(Tag.get_tag_by_id(t))
        return tags
