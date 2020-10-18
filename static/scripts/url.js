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