const initDatas = async (id=6) => {
    store.id = id;

    store.tasks = await get_task_list(id);
    store.tasks.forEach(task => task_create(task.deadline, task.short_desc, task.dash, task.difficulty));

    store.tashboards = await getTashboards(id);
    store.tashboards.forEach(tashboard => makeListDashboardsItem(tashboard.id, tashboard.name));
}

window.addEventListener("load", () => {
    initDatas(7);
});