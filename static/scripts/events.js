// window.addEventListener("load", () => {
//     Tree.drawTree(tree);
// });

const optionsContainer = document.querySelector(".options_container");

document.querySelector(".selected").addEventListener("click", () => {
    optionsContainer.classList.add("active");
})

// const isClickInOptionsContainer = (target) => {
//     if (target.tagName === "BODY") {
//         return false;
//     }

//     return target.classList.contains("options_container") ||
//         target.classList.contains("selected") ||
//         isClickInOptionsContainer(target.parentElement)
// }

// const toggleOptionsContainer = (target) => {
//     if (!isClickInOptionsContainer(target)) {
//         optionsContainer.classList.remove("active");
//     }
// }

// window.addEventListener("click", (e) => {
//     toggleOptionsContainer(e.target);
// });

const postPost = async () => {
    const responce = await fetch("/delete_task", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: body
    });

    console.log(await responce.json());
}