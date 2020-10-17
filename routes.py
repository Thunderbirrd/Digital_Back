from app import app
from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task, Tag, TaskTable, TaskTag, TaskChildren
import json
import datetime


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
            all_tasks_tables_id = []
            all_users_dashboards = []
            ex = Task.get_all_tasks_by_executor_id(user.id)
            lead = Task.get_all_tasks_by_leader_id(user.id)
            for task in ex:
                if all_tasks_tables_id.count(task.taskboard_id) == 0:
                    all_tasks_tables_id.append(task.taskboard_id)
            for task in lead:
                if all_tasks_tables_id.count(task.taskboard_id) == 0:
                    all_tasks_tables_id.append(task.taskboard_id)
            for i in all_tasks_tables_id:
                task_table = TaskTable.get_task_table_by_id(i)
                all_users_dashboards.append({"id": i, "name": task_table.name})
            d = {
                "id": user.id,
                "login": user.login,
                "name": user.name,
                "surname": user.surname,
                "lastname": user.lastname,
                "all_users_dashboards": all_users_dashboards
            }
            return json.dumps(d)
        else:
            return "Wrong login and/or password"


@app.route('/createChild', methods=['POST'])
def create_child():
    if request.form:
        parent = request.form.get("idParentTask")
        leader = request.form.get("leader")
        executor = request.form.get("executor")
        deadline = request.form.get("deadline")
        short_desc = request.form.get("short_desc")
        desc = request.form.get("desc")
        intensity = request.form.get("difficulty")
        tags = request.form.get("tags")
        parent = Task.get_task_by_id(parent)
        parent_id = parent.id
        task = Task(leader, parent.taskboard_id, deadline, short_desc, intensity, parent_id, executor, desc, False)
        task.save()
        task_children = TaskChildren(parent_id, task.id)
        task_children.save()
        tags = tags.split(",")
        for tag in tags:
            task_tag = TaskTag(int(task.id), int(tag))
            task_tag.save()
        return json.dumps({"id": task.id})


@app.route('/getListTask', methods=['POST'])
def get_task_list():
    if request.form:
        user_id = int(request.form.get("id"))
        tasks = []
        lead = Task.get_all_tasks_by_leader_id(user_id)
        ex = Task.get_all_tasks_by_executor_id(user_id)
        print(lead)
        print(ex)
        if lead:
            for le in lead:
                task = Task.get_task_by_id(le)
                tags = list(TaskTag.get_all_tasks_tags(task.id))
                tasks.append({
                    "id": task.id,
                    "isSingleTask": task.is_single_task,
                    "leader": task.leader,
                    "executor": task.executor,
                    "shortdescription": task.short_desc,
                    "deadline": task.deadline.strftime("%Y-%m-%d"),
                    "difficulty": task.intensity,
                    "tasktableid": task.taskboard_id,
                    "tags": tags
                })
        if ex:
            for e in ex:
                task = Task.get_task_by_id(e)
                tags = list(TaskTag.get_all_tasks_tags(task.id))
                for i in range(len(tags)):
                    tags[i] = {"id": tags[i].id, "name": tags[i].name}
                tasks.append({
                    "id": task.id,
                    "isSingleTask": task.is_single_task,
                    "leader": task.leader,
                    "executor": task.executor,
                    "shortdescription": task.short_desc,
                    "deadline": task.deadline.strftime("%Y-%m-%d"),
                    "difficulty": task.intensity,
                    "tasktableid": task.taskboard_id,
                    "tags": tags
                })
        print(tasks)
        return json.dumps(tasks)


@app.route('/', methods=['GET'])
def index():
    return "Hello, world"
