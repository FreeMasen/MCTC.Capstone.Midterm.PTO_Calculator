window.addEventListener('onload', () => {
    registerTextBoxes()
});

function registerTextBoxes() {
    console.log('registerTextBoxes')
    let textBoxes = document.querySelectorAll('.text-box-input');
    for (var i = 0; i < textBoxes.length;i++) {
        textBoxes[i].addEventListener('focus', textBoxFocus);
        textBoxes[i].addEventListener('blur', textBoxFocus);
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
    if (!textbox) return;
    let textBoxContainer = textbox.parentElement;
    if (!textBoxContainer) return;
    return textBoxContainer.querySelector('.active-bar');
}