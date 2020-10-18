const list_new_task = document.querySelector(".list_new_task");

document.querySelector(".managment_buttons_add").addEventListener("click", () => {
    list_new_task.classList.remove("hide");
});

document.querySelector(".list_task_button").addEventListener("click", async () => {
    const short_desc = document.querySelector(".list_task_input1").value;
    const desc = document.querySelector(".list_task_input2").value;

    const ch = document.getElementById("checking").value;
    const ex = document.getElementById("executor").value;

    const leader = await get_user_id_by_login(ch);
    const executor = await get_user_id_by_login(ex);

    const difficulty = document.getElementById("rangeValue").textContent;
    const deadline = document.getElementById("deadline").value;

    await create_single_task(short_desc, desc, leader, executor, difficulty, deadline, "");

    store.tasks = await get_task_list(store.id);
    store.tasks.forEach(task => task_create(task.deadline, task.short_desc, task.dash, task.difficulty));
});

function task_create(deadline, short_desc, dash, difficulty){
    const li = document.createElement("li")
    li.classList.add("tasks")
    const div1 = document.createElement("div")
    div1.classList.add("tasks_description")
    const p1 = document.createElement("p")
    p1.classList.add("deadline")
    const div2 = document.createElement("div")
    div2.classList.add("descrip")
    const p2 = document.createElement("p")
    p2.classList.add("dash")
    const p3 = document.createElement("p")
    p3.classList.add("task")
    const div3 = document.createElement("div")
    div3.classList.add("duff")


    div2.appendChild(p2)
    div2.appendChild(p3)
    div1.appendChild(p1)
    div1.appendChild(div2)
    li.appendChild(div1)
    li.appendChild(div3)

    for(let i = 0; i < difficulty; i++){
        const div4 = document.createElement("div")
        div4.classList.add("level")
        div3.appendChild(div4)
    }

    p1.textContent = deadline
    p2.textContent = dash
    p3.textContent = short_desc

    document.querySelector(".list_tasks ul").appendChild(li)
}
// input_create_tag
document.querySelector("#button_create_tag").addEventListener("click", async() =>{
    const span = document.createElement("span")
    span.classList.add("list_task_tag")
    const button = document.createElement("button")
    const name = document.getElementById("input_create_tag").value
    const p = document.getElementById("p_id")
    let id = await create_tag(name, store.id)

    span.textContent = name
    span.appendChild(button)
    p.appendChild(button)
    button.addEventListener("click", async ()=> {
        span.style.display = "none"
        deleteTag(id)
    })


})