"use strict"

const csrfToken = document.cookie.split('; ').find(row => row.startsWith("csrftoken="))?.split('=')[1];
console.log(csrfToken)
const labId = document.querySelector('#lab-title').dataset.id
const expertsSection = document.querySelector('#experts-section')
const permissionsSection = document.querySelector('#permissions-section')

let experts = [];
let permissions = [];





async function getExperts() {
    const endpoint = {parent: "experts_lab", child: "expert"};
    const URL = `http://127.0.0.1:8000/api/${endpoint.parent}/${labId}/`;
    const dellButtonClass = "expert-del-button"
    const result = await fetch(URL, {
        method: 'GET',
        credentials: 'include',
    });
    experts = await result.json();
    console.log(experts);
    experts.forEach(expert => {
        expertsSection.innerHTML += `<div>${expert.pk} ${expert.name} <button class ="${dellButtonClass}" data-item-id="${expert.pk}">Удалить</button></div>`
    })
    bindDelButtons(dellButtonClass, endpoint)
}

function bindDelButtons(buttonClass, endpoint) {
    
    const deleteButtons = expertsSection.querySelectorAll(`button.${buttonClass}`)
    console.log(deleteButtons)
    deleteButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const URL = `http://127.0.0.1:8000/api/${endpoint.parent}/${labId}/${endpoint.child}/${button.dataset.itemId}/delete/`;
            const result = await fetch(URL, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });
            if (result.status === 200) {
                button.parentNode.remove()
            }
        })
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



getExperts();
getPermissions()