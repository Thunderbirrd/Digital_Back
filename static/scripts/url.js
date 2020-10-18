const register = async (login, password, name, surname, lastname) => {
    const responce = await fetch("/register", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({login, password, name, surname, lastname})
    });
    return await responce.json();
}


const get_user_id_by_login = async (login) => {
    const responce = await fetch("/get_user_id_by_login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({login})
    });
    return await responce.json();
}


const login = async (login, password) => {
    const responce = await fetch("/login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({login, password})
    });
    return responce;
}


const create_child = async (parent, leader, executor, deadline, short_desc, desc, difficulty, tags) => {
    const responce = await fetch("/createChild", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({parent, leader, executor, deadline, short_desc, desc, difficulty, tags})
    });
    return await responce.json();
}


const get_task_by_id = async (id) => {
    const responce = await fetch("/get_task_by_id", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}


const get_tag_by_id = async (id) => {
    const responce = await fetch("/get_tag_by_id", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}


const get_task_list = async (id) => {
    const responce = await fetch("/getListTask", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}


const create_tag = async (name, user_id) => {
    const responce = await fetch("/create_tag", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({name, user_id, tasktable_id: 0})
    });
    return await responce.json();
}


const create_board = async (admin, name, short_desc, leader, executor, difficulty, desc, deadline, tags) => {
    const responce = await fetch("/create_board", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({admin, name, short_desc, leader, executor, difficulty, desc, deadline, tags})
    });
    return await responce.json();
}


const change_task_status = async (id) => {
    const responce = await fetch("/change_task_status", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}


const create_single_task = async (short_desc, desc, leader, executor, difficulty, deadline, tags) => {
    const responce = await fetch("/create_single_task", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({short_desc, desc, leader, executor, difficulty, deadline, tags})
    });
    return await responce.json();
}


const get_tree = async (id) => {
    const responce = await fetch("/get_tree", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}


const delete_task = async (id) => {
    const responce = await fetch("/delete_task", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });
    return await responce.json();
}

const getTashboards = async (id) => {
    const responce = await fetch("/get_boards", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });

    return await responce.json();
}

const deleteTag = async (id) => {
    const responce = await fetch("/delete_tag", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({id})
    });

    return await responce.json();
}
