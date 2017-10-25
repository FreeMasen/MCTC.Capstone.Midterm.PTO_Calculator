window.addEventListener('DOMContentLoaded', () => {
    registerUsername();
    setDefultDate();
    registerClearButton();
    registerRoleCheckboxes();
});

function registerUsername() {
    let username = document.querySelector('#username');
    if (!username) return;
    username.addEventListener('focus', insertDefaultUsername);
}

function registerClearButton() {
    let clearButton = document.querySelector('#clear');
    if (!clearButton) return;
    clearButton.addEventListener('click', clearCheckBoxes);
}

function registerRoleCheckboxes() {
    let checkboxes = document.querySelectorAll('.role-selection');
    for (let box of checkboxes) {
        box.addEventListener('change', roleChanged);
    }
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



function clearCheckBoxes() {
    let deleteBoxes = document.querySelectorAll('[name="delete-user"]');
    for (let box of deleteBoxes) {
        box.checked = false;
    }
}

function clearAllChanges() {
    let trackers = document.querySelectorAll('.#change-tracker');
    for (let tracker of trackers) {
        let changes = JSON.parse(tracker.value);
    }
}

function roleChanged(event) {
    let box = event.currentTarget;
    if (!box) return;
    let boxValues = box.id.split('-')
    let empId = boxValues[0];
    let roleName = boxValues[1];
    let change = new Change(roleName, box.checked, box.id, empId);
    let existingChanges = getChanges(empId);
    let updatedChanges = updateChanges(existingChanges, change);
    saveChanges(empId, updatedChanges);
}

function getChanges() {
    let changeInput = document.querySelector(`#change-tracker`);
    if (!changeInput || changeInput.value == '') return [];
    return JSON.parse(changeInput.value);
}

function saveChanges(empId, changes) {
    console.log('saveChanges', changes);
    let changeInput = document.querySelector(`#change-tracker`);
    if (!changeInput) return;
    changeInput.value = JSON.stringify(changes);
}

function updateChanges(existingChanges, newChange) {
    let thisUsersChanges = existingChanges.filter(c => c.empId === newChange.empId);
    for (let c of thisUsersChanges) {
        if (c.role === newChange.role) {
            return existingChanges.filter(ch => ch.role !== newChange.role);
        }
    }
    existingChanges.push(newChange);
    return existingChanges;
}

function Change(role, checked, checkboxId, empId) {
    this.role = role;
    this.checked = checked,
    this.checkboxId = checkboxId,
    this.empId = empId
}
