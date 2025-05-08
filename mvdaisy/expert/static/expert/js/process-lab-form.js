"use strict"
console.log("process-lab-form.js")

const labId = document.querySelector('#lab-title').dataset.id
const expertsSection = document.querySelector('#experts-section')
const permissionsSection = document.querySelector('#permissions-section')

let experts = [];
let permissions = [];


async function getExperts() {
    const URL = `http://127.0.0.1:8000/api/experts_lab/${labId}/`;
    const result = await fetch(URL, {
        method: 'GET',
        credentials: 'include',
    });
    experts = await result.json();
    console.log(experts);
    experts.forEach(expert => {
        expertsSection.innerHTML += `<div>${expert.pk} ${expert.name}</div>`
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