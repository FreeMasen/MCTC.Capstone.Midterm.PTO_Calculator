window.addEventListener('DOMContentLoaded', () => {
    registerUsername();
    setDefultDate();
    registerClearButton();
});

function registerUsername() {
    let username = document.querySelector('#username');
    if (!username) return;
    username.addEventListener('focus', insertDefaultUsername);
}

function insertDefaultUsername(event) {
    let input = event.currentTarget;
    if (input.value != '') return;
    let fNameInput = document.querySelector('#first-name');
    let lNameInput = document.querySelector('#last-name');
    let firstName = fNameInput.value;
    let firstInitial = firstName.substr(0,1);
    let lastName = lNameInput.value;
    let username = `${firstInitial}${lastName}`;
    input.value = username;
    input.setSelectionRange(0, username.length);
}

function setDefultDate() {
    let hireDate = document.querySelector('#hire-date');
    if (!hireDate) return;
    hireDate.value = new Date().toISOString().split('T')[0];;
}

function registerClearButton() {
    let clearButton = document.querySelector('#clear');
    if (!clearButton) return;
    clearButton.addEventListener('click', clearCheckBoxes);
}

function clearCheckBoxes() {
    let deleteBoxes = document.querySelectorAll('[name="delete-user"]');
    for (let box of deleteBoxes) {
        box.checked = false;
    }
}