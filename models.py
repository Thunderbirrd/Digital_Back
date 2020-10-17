from database import db


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


class Tag(db.Model, Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    taskboard_id = db.Column(db.Integer, db.ForeignKey(TaskTable.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name):
        self.name = name
        self.save()

    @staticmethod
    def get_tag_by_id(i):
        return db.session.query(Tag.id).filter(Tag.id == i).first()

    @staticmethod
    def get_all_task_boards_tags(task_board_id):
        return db.session.query(Tag.taskboard_id).filter(Tag.taskboard_id == task_board_id).all()

    @staticmethod
    def get_all_users_tags(id_user):
        return db.session.query(Tag.user_id).filter(Tag.user_id == id_user).all()


class Task(db.Model, Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    short_desc = db.Column(db.String(), nullable=False)
    leader = db.Column(db.Integer, db.ForeignKey(User.id))
    parent = db.Column(db.Integer, db.ForeignKey(id))
    executor = db.Column(db.Integer, db.ForeignKey(User.id))
    taskboard_id = db.Column(db.Integer, db.ForeignKey(TaskTable.id), nullable=False)
    intensity = db.Column(db.Integer)
    desc = db.Column(db.String)
    deadline = db.Column(db.Date)
    is_single_task = db.Column(db.Boolean)

    def __init__(self, leader, taskboard_id, deadline, short_desc, intensity, parent=0, executor=0, desc="",
                 is_single=False):
        self.leader = leader
        self.parent = parent
        self.executor = executor
        self.taskboard_id = taskboard_id
        self.intensity = intensity
        self.short_desc = short_desc
        self.desc = desc
        self.deadline = deadline
        self.is_single_task = is_single
        self.save()

    @staticmethod
    def get_task_by_id(i):
        return db.session.query(Task.id).filter(Task.id == i).first()

    @staticmethod
    def get_task_by_short_desc(desc):
        return db.session.query(Task.short_desc).filter(Task.short_desc == desc).first()

    @staticmethod
    def get_all_tasks_by_executor_id(i):
        return db.session.query(Task.executor).filter(Task.executor == i).all()

    @staticmethod
    def get_all_tasks_by_leader_id(i):
        return db.session.query(Task.leader).filter(Task.leader == i).all()

    @staticmethod
    def get_all_task_boards_tasks(i):
        return db.session.query(Task.taskboard_id).filter(Task.taskboard_id == i).all()


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


class TaskChildren(db.Model, Model):
    __tablename__ = "task_children"
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, db.ForeignKey(Task.id))
    child = db.Column(db.Integer, db.ForeignKey(Task.id))

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.save()

    @staticmethod
    def get_all_children(parent):
        all_children = db.session.query(TaskChildren.parent).filter(TaskChildren.parent == parent).all()
        children_ids = []
        for task in all_children:
            children_ids.append(task.child)
        children = []
        for i in children_ids:
            children.append(Task.get_task_by_id(i))
        return children


class UserTag(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id))
    id_tag = db.Column(db.Integer, db.ForeignKey(Tag.id))

    def __init__(self, user, tag):
        self.id_user = user
        self.id_tag = tag
        self.save()

    @staticmethod
    def get_all_users_tags(user_id):
        manytomany = db.session.query(UserTag.id_user).filter(TaskTag.id_user == user_id).all()
        tag_id = []
        for t in manytomany:
            tag_id.append(t.id_tag)
        tags = []
        for t in tag_id:
            tags.append(Tag.get_tag_by_id(t))
        return tags