const list_dashboards_list = document.querySelector(".list_dashboards_list");
const list_dashboards_add = list_dashboards_list.querySelector(".list_dashboards_add");

const makeListDashboardsItem = (id, name) => {
    const li = document.createElement("li");
    li.classList.add("list_dashboards_item");

    const span = document.createElement("span");
    span.textContent = name;
    li.appendChild(span)

    li.addEventListener("click", async () => {
        document.querySelector(".wrap_tree").classList.remove("hide");
        const data = await get_tree(id);
        Tree.drawTree(transformTree(data));
    })

    list_dashboards_list.insertBefore(li, list_dashboards_add);
}

const transformTree = (data) => {
    const root = data.find(node => node.parent === null);
    
    getChildren(root, data)

    return root;
}

const getChildren = (root, data) => {
    data.forEach(node => {
        if (node.parent === root.id) {
            root.children.push(node);
        }
    });

    root.children.forEach(node => {
        getChildren(node, data);
    });
}

const class_create_table = document.querySelector(".class_create_table");
const input_create_table = document.getElementById("input_create_table");
const button_create_table = document.getElementById("button_create_table");

list_dashboards_add.addEventListener("click", () => {
    class_create_table.classList.remove("hide");
});

button_create_table.addEventListener("click", async () => {
    class_create_table.classList.add("hide");

    
});