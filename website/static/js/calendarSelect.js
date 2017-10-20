window.addEventListener('load', registerDates)

function registerDates() {
    console.log('registering dates')
    let days = document.querySelectorAll('.day');
    console.log(days);
    for (let day of days) {
        day.addEventListener('click', dayClicked);
    }
}

function dayClicked(event) {
    let dayDiv = event.currentTarget;
    console.log('dayClicked', dayDiv.innerHTML);
    return dayDiv.innerHTML
}

function addDay(number) {
    //find start-date if empty
    //put it there
    //otherwise check if this date
    //is before the other
    //if so, replace it
    //if not, find the end date
    //add this value there
}