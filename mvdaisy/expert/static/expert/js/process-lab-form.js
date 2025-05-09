"use strict"

const csrfToken = document.cookie.split('; ').find(row => row.startsWith("csrftoken="))?.split('=')[1];
console.log(csrfToken)

const globalData = {};




async function getRelation(endpoint, labId, delButtonClass, section) {
    const URL = `http://127.0.0.1:8000/api/${endpoint.parent}/${labId}/`;
    const result = await fetch(URL, {
        method: 'GET',
        credentials: 'include',
    });
    const items = await result.json();
    globalData[endpoint.child] = items
    console.log(items);
    items.forEach(item => {
        section.innerHTML += `<div>${item.pk} ${item.name} <button class ="row-button ${delButtonClass}" data-item-id="${item.pk}">Удалить</button></div>`
    })
    bindDelButtons(endpoint, labId, delButtonClass, section)
}

async function deleteRelation( endpoint, labId, button){
    const URL = `http://127.0.0.1:8000/api/${endpoint.parent}/${labId}/${endpoint.child}/${button.dataset.itemId}/delete/`;
    const result = await fetch(URL, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    });
    if (result.status === 204) {
        button.parentNode.remove()
    }
}

function bindDelButtons(endpoint, labId, delButtonClass, section) {    
    const deleteButtons = section.querySelectorAll(`button.${delButtonClass}`)
    console.log(deleteButtons)
    deleteButtons.forEach(button => {
        button.addEventListener('click', async () => await deleteRelation(endpoint, labId, button))
    })

}



async function getPermissions() {
    const URL = `http://127.0.0.1:8000/api/ex_area_lab/${labId}/`;
    const result = await fetch(URL, {
        method: 'GET',
        credentials: 'include',
    });
    permissions = await result.json();
    console.log(permissions);
    permissions.forEach(permission => {
        permissionsSection.innerHTML += `<div>${permission.pk} ${permission.name}</div>`
    })
}

async function openExpertModal(expertModal, labId) {
    const selectContainer = expertModal.querySelector(".modal-body")
    selectContainer.innerHTML = ""
    const selectElement = document.createElement("select")
    
    const result = await fetch(`http://127.0.0.1:8000/api/experts_not_assigned/${labId}/`, {
        method: 'GET',
        credentials: 'include',
    })
    const experts = await result.json();
    selectElement.innerHTML += `<option value="" selected disabled>---</option>`
    experts.forEach(expert => {
        selectElement.innerHTML += `<option value="${expert.pk}">${expert.name}</option>`
    })
    selectContainer.appendChild(selectElement)
    console.log(selectElement)
    
    expertModal.style.display = "block";
}

async function addExpert(expertModal, labId) {
    const expertId = expertModal.querySelector("select").value
    if (expertId === "") return
    const result = await fetch(`http://127.0.0.1:8000/api/experts_lab/expert/create/`, {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken,},
        body: JSON.stringify({laboratory: labId, expert: expertId}),
    })
    expertModal.style.display = "none";

}


const process = () => {
    const labId = document.querySelector('#lab-title').dataset.id
    const expertsSection = document.querySelector('#experts-section')
    const permissionsSection = document.querySelector('#permissions-section')
    const expertModal = document.querySelector('#id-modal-expert')    
    const addExpertButton = document.querySelector('#add-expert-button')
    const permissionModal = document.querySelector('#id-modal-permission')
    const addPermissionButton = document.querySelector('#add-permission-button')
    const confirmPermissionButton = document.querySelector('#confirm-permission-button')
    const confirmExpertButton = document.querySelector('#confirm-expert-button')


    getRelation({parent: "experts_lab", child: "expert"}, labId,  "expert-del-button", expertsSection);
    getRelation({parent: "ex_area_lab", child: "permission"}, labId,  "permission-del-button", permissionsSection);


    addPermissionButton.addEventListener('click', () => {
        permissionModal.style.display = "block";
    })

    addExpertButton.addEventListener('click', () => openExpertModal(expertModal, labId));
    confirmExpertButton.addEventListener('click', () => addExpert(expertModal, labId));

    expertModal.addEventListener('click', (event) => {
        if (event.target === expertModal) {
            expertModal.style.display = "none";
        }
    })
    permissionModal.addEventListener('click', (event) => {
        if (event.target === permissionModal) {
            permissionModal.style.display = "none";
        }
    })

}

/*класс, пердставляющий собой модальное окно, в котором появляется выпадающий список экспертов. При выборе эксперта нажо нажать на кнопку добавить, после чего на сервер отправляется запрос с id эксперта  */


document.addEventListener('DOMContentLoaded', process);