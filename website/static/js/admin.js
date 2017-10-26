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

function registerClearButton() {
    let clearButton = document.querySelector('#clear');
    if (!clearButton) return;
    clearButton.addEventListener('click', () => {
        clearCheckBoxes();
        clearChanges();
    });
}

function clearCheckBoxes() {
    let deleteBoxes = document.querySelectorAll('[name="delete-user"]');
    for (let box of deleteBoxes) {
        box.checked = false;
    }
}

function clearChanges() {
    let changes = getChanges();
    for (let change of changes) {
        let box = document.getElementById(change.inputId);
        box.checked = !change.state
    }
    saveChanges([]);
}

function registerRoleCheckboxes() {
    let boxes = document.querySelectorAll('.role-selection');
    for (let box of boxes) {
        box.addEventListener('change', roleChanged);
    }
}

function roleChanged(event) {
    let box = event.currentTarget;
    let boxValues = box.id.split('-');
    let role = boxValues[0];
    let empId = boxValues[1];
    let change = new Change(empId, role, box.checked, box.id);
    let changes = getChanges();
    let updatedChanges = updateChanges(changes, change);
    saveChanges(updatedChanges);
}

function updateChanges(oldChanges, newChange) {
    for (let i = 0; i < oldChanges.length;i++) {
        let change = oldChanges[i];
        if (change.role == newChange.role &&
            change.empId == newChange.empId) {
            oldChanges.splice(i,1);
            return oldChanges;
        }
    }
    return oldChanges.concat([newChange]);
}

function getChanges() {
    let tracker = document.querySelector('#change-tracker');
    if (!tracker || tracker.value == '') return [];
    return JSON.parse(tracker.value);
}

function saveChanges(changes) {
    let tracker = document.querySelector('#change-tracker');
    if (!tracker) return;
    tracker.value = JSON.stringify(changes);
}

function Change(empId, role, state, inputId) {
    this.empId = empId;
    this.role = role;
    this.state = state;
    this.inputId = inputId;
}
