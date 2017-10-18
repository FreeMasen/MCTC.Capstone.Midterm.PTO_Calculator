window.addEventListener('load', () => {
    registerTextBoxes();
});

function registerTextBoxes() {
    let textBoxes = document.querySelectorAll('input');
    for (var i = 0; i < textBoxes.length;i++) {
        textBoxes[i].addEventListener('focus', textBoxFocus);
        textBoxes[i].addEventListener('blur', textBoxBlur);
    }
}

function textBoxFocus(event) {
    let textbox = event.currentTarget;
    let activeBar = getActiveBar(textbox);
    if (!activeBar) return;
    activeBar.setAttribute('class', activeBar.className + ' active');
}

function textBoxBlur(event) {
    let textbox = event.currentTarget;
    let activeBar = getActiveBar(textbox);
    if (!activeBar) return;
    activeBar.setAttribute('class', activeBar.className.replace(' active', ''));
}

function getActiveBar(input) {
    let textBoxContainer = input.parentElement;
    if (!textBoxContainer) return;
    return textBoxContainer.querySelector('.active-bar');
}