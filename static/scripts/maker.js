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
