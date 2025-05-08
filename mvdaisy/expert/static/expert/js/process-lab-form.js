"use strict"

const csrfToken = document.cookie.split('; ').find(row => row.startsWith("csrftoken="))?.split('=')[1];
console.log(csrfToken)

let experts = [];
let permissions = [];





async function getRelation(endpoint, labId, delButtonClass, section) {
    const URL = `http://127.0.0.1:8000/api/${endpoint.parent}/${labId}/`;
    const result = await fetch(URL, {
        method: 'GET',
        credentials: 'include',
    });
    const items = await result.json();
    console.log(items);
    items.forEach(item => {
        section.innerHTML += `<div>${item.pk} ${item.name} <button class ="${delButtonClass}" data-item-id="${item.pk}">Удалить</button></div>`
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

const process = () => {
    const labId = document.querySelector('#lab-title').dataset.id
    const expertsSection = document.querySelector('#experts-section')
    const permissionsSection = document.querySelector('#permissions-section')

    getRelation({parent: "experts_lab", child: "expert"}, labId,  "expert-del-button", expertsSection);
    getRelation({parent: "ex_area_lab", child: "permission"}, labId,  "permission-del-button", permissionsSection);}

document.addEventListener('DOMContentLoaded', process);