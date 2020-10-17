from app import app
from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task, Tag, TaskTable, TaskTag, TaskChildren
import json


@app.route('/register', methods=['POST'])
def register():
    if request.data:
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


@app.route('/get_user_id_by_login', methods=['POST'])
def get_user_id_by_login():
    if request.data:
        user_login = request.form.get("login")
        user = User.get_user_by_login(user_login)
        if user:
            return str(user.id)
        else:
            return "No such user"


@app.route('/login', methods=['POST'])
def login():
    if request.data:
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
                if all_tasks_tables_id.count(task.taskboard_id) == 0 and task.taskboard_id:
                    all_tasks_tables_id.append(task.taskboard_id)
            for task in lead:
                if all_tasks_tables_id.count(task.taskboard_id) == 0 and task.taskboard_id:
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
    if request.data:
        parent = request.form.get("parent")
        leader = request.form.get("leader")
        executor = request.form.get("executor")
        deadline = request.form.get("deadline")
        short_desc = request.form.get("short_desc")
        desc = request.form.get("desc")
        intensity = request.form.get("difficulty")
        tags = request.form.get("tags")
        parent = Task.get_task_by_id(int(parent))
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


@app.route('/get_task_by_id', methods=['POST'])
def get_task_by_id():
    if request.data:
        task = request.form.get("id")
        task = Task.get_task_by_id(task)
        tags = list(TaskTag.get_all_tasks_tags(task.id))
        for i in range(len(tags)):
            tags[i] = {"id": tags[i].id, "name": tags[i].name}
        children = list(TaskChildren.get_all_children(task.id))
        for i in range(len(children)):
            children[i] = {"id": children[i].id, "short_desc": children[i].short_desc}
        d = {
            "id": task.id,
            "short_desc": task.short_desc,
            "leader": task.leader,
            "parent": task.parent,
            "executor": task.executor,
            "taskboard_id": task.taskboard_id,
            "intensity": task.intensity,
            "desc": task.desc,
            "deadline": task.deadline.strftime("%Y-%m-%d"),
            "is_single_task": task.is_single_task,
            "tags": tags,
            "children": children
        }
        return json.dumps(d)


@app.route('/get_tag_by_id', methods=['POST'])
def get_tag_by_id():
    if request.data:
        tag = request.form.get("id")
        tag = Tag.get_tag_by_id(tag)
        return {
            "id": tag.id,
            "name": tag.name,
            "tasktable_id": tag.tasktable_id,
            "user_id": tag.user_id
        }


@app.route('/getListTask', methods=['POST'])
def get_task_list():
    if request.data:
        user_id = int(request.form.get("id"))
        tasks = []
        lead = Task.get_all_tasks_by_leader_id(user_id)
        ex = Task.get_all_tasks_by_executor_id(user_id)
        if lead:
            for le in lead:
                task = Task.get_task_by_id(le.id)
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
        if ex:
            for e in ex:
                task = Task.get_task_by_id(e.id)
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
        return json.dumps(tasks)


@app.route('/', methods=['GET'])
def index():
    return "Hello, world"


@app.route('/create_tag', methods=['POST'])
def create_tag():
    if request.data:
        name = request.form.get("name")
        tasktable_id = request.form.get("tasktable_id")
        user_id = request.form.get("user_id")
        if int(tasktable_id) != 0:
            tag = Tag(name, tasktable_id)
            tag.save()
            return str(tag.id)
        elif int(user_id) != 0:
            tag = Tag(name, None, user_id)
            tag.save()
            return str(tag.id)
        else:
            return "Error"


@app.route('/create_board', methods=['POST'])
def create_board():
    if request.data:
        admin = request.form.get("admin")
        name = request.form.get("name")
        table = TaskTable(name, admin)
        table.save()
        short_desc = request.form.get("short_desc")
        leader = request.form.get("leader")
        executor = request.form.get("executor")
        taskboard_id = table.id
        intensity = request.form.get("difficulty")
        desc = request.form.get("desc")
        deadline = request.form.get("deadline")
        is_single_task = False
        task = Task(leader, taskboard_id, deadline, short_desc, intensity, None, executor, desc, is_single_task)
        task.save()
        for tag in str(request.form.get("tags")).split(","):
            TaskTag(task.id, int(tag))

        return json.dumps({"taskid": task.id, "tableid": table.id})


@app.route('/change_task_status', methods=['POST'])
def change_task_status():
    if request.data:
        task_id = request.form.get("id")
        task = Task.get_task_by_id(task_id)
        if task:
            task.change_task_status()
            task.save()
            return f"New task status is {task.done}"
        else:
            return "No such task"


@app.route('/create_single_task', methods=['POST'])
def create_single_task():
    if request.data:
        short_desc = request.form.get("short_desc")
        desc = request.form.get("desc")
        leader = int(request.form.get("leader"))
        executor = int(request.form.get("executor"))
        intensity = int(request.form.get("difficulty"))
        deadline = request.form.get("deadline")
        tags = request.form.get("tags")
        task = Task(leader, None, deadline, short_desc, intensity, None, executor, desc, True, False)
        task.save()
        tags = tags.split(",")
        for tag in tags:
            task_tag = TaskTag(task.id, tag)
            task_tag.save()

        return json.dumps({"id": task.id})


@app.route('/get_tree', methods=['POST'])
def get_tree():
    if request.data:
        task_table = request.form.get("id")
        tasks = Task.get_all_task_boards_tasks(int(task_table))
        d = []
        for task in tasks:
            tags = list(TaskTag.get_all_tasks_tags(task.id))
            for i in range(len(tags)):
                tags[i] = {"id": tags[i].id, "name": tags[i].name}
            children = list(TaskChildren.get_all_children(task.id))
            for i in range(len(children)):
                children[i] = {"id": children[i].id, "short_desc": children[i].short_desc}
            d.append({
                "id": task.id,
                "isSingleTask": task.is_single_task,
                "leader": task.leader,
                "executor": task.executor,
                "shortdescription": task.short_desc,
                "deadline": task.deadline.strftime("%Y-%m-%d"),
                "difficulty": task.intensity,
                "tasktableid": task.taskboard_id,
                "tags": tags,
                "children": children
            })

        return json.dumps(d)


@app.route('/delete_task', methods=['POST'])
def delete_task():
    if request.data:
        task_id = json.loads(request.data)["id"]
        task = Task.get_task_by_id(task_id)
        if task:
            task.delete()
            return json.dumps("Task deleted successfully")
        else:
            return json.dumps("No such task")
