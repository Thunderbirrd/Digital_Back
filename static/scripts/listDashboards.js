const list_dashboards_list = document.querySelector(".list_dashboards_list");
const list_dashboards_add = list_dashboards_list.querySelector(".list_dashboards_add");

const makeListDashboardsItem = (id, name) => {
    const li = document.createElement("li");
    li.classList.add("list_dashboards_item");

    const span = document.createElement("span");
    span.textContent = name;
    li.appendChild(span)

    li.addEventListener("click", async () => {
        Tree.drawTree(await get_tree(id));
    })

    list_dashboards_list.insertBefore(li, list_dashboards_add);
}