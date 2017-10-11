window.addEventListener('onload', () => {
    console.log('window loaded');
    registerTextBoxes();
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
    console.log('textBoxFocus', element.currentTarget);
    let textbox = event.currentTarget;
    let activeBar = getActiveBar(textbox);
    if (!activeBar) return;
    activeBar.setAttribute('class', activeBar.className + ' active');
}

function textBoxBlur(event) {
    console.log('textBoxBlur', element.currentTarget);
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