function log(...args) {
    console.log('debug->', new Date(), ...args);
}
window.addEventListener('DOMContentLoaded', () => {
    registerDates();
    registerNavLinks();
    registerInputs();
    if (!window.history.state) {
        updateUrl(getMonth(), getYear());
    }
    window.addEventListener('popstate', (event) => {
        if (!event.state) return;
        goToMonth(event.state.month,
                    event.state.year)
    });
});

function registerDates() {
    let days = document.querySelectorAll('.day');
    for (let day of days) {
        day.addEventListener('click', dayClicked);
    }
}

function registerNavLinks() {
    let links = document.querySelectorAll('.calendar-nav');
    for (let link of links) {
        link.addEventListener('click', changeMonth);
    }
}

function registerInputs() {
    const observer = new MutationObserver(dayChanged);
    let inputs = document.querySelectorAll('input[type="hidden"]');
    for (let input of inputs) {
        observer.observe(input, {
            attributes: true
        });
    }
}

function dayClicked(event) {
    let day = event.currentTarget.innerHTML;
    let month = getMonth();
    let year = getYear();
    let newDay = new Day(month, day, year);
    addDay(newDay);
}

function getMonth() {
    let month = document.querySelector('#month');
    return month.value;
}

function setMonth(month) {
    let monthInput = document.querySelector('#month');
    if (!monthInput) return;
    monthInput.setAttribute('value', month);
}

function setYear(year) {
    let yearInput = document.querySelector('#year');
    if (!yearInput) return;
    yearInput.setAttribute('value', year);
}

function getYear() {
    let year = document.querySelector('#year');
    return year.value;
}

function getStart() {
    return getDay('start-day');
}

function getEnd() {
    return getDay('end-day');
}

function addDay(day) {
    //try and get the start day
    let start = getDay('start-day');
    //if none
    if (!start) {
        //set the start day
        return setDay('start-day', day);
    }
    //try and get the end day
    let end = getDay('end-day');
    if (!end) {
        return setDay('end-day', day);
    }
    //reset the end day to empty
    setDay('end-day', '');
    //insert the new day into the start day
    setDay('start-day', day);
}

function setDay(id, day) {
    let input = document.querySelector(`#${id}`);
    if (!input) return displayMessage('Something has gone wrong, please try again.');
    input.setAttribute('value', day.toString())
}

function getDay(id) {
    let dayBox = document.querySelector(`#${id}`);
    if (!dayBox) return
    if (dayBox.value != '') {
        return Day.fromString(dayBox.value);
    }
}

function Day(month = '1', day = '1', year = '1970') {
    this.month = parseInt(month);
    this.day = parseInt(day);
    this.year = parseInt(year);
}

Day.prototype.toString = function() {
    return `${this.month || 1}-${this.day || 1}-${this.year || 1970}`
}

Day.fromString = function(dayString) {
    let parts = dayString.split('-');
    return new Day(parts[0], parts[1], parts[2]);
}

Day.prototype.greaterThan = function(otherDay) {
    if (!otherDay) return false;
    if (this.year < otherDay.year) {
        return false;
    }
    if (this.year > otherDay.year) {
        return true;
    }
    if (this.month < otherDay.month) {
        return false;
    }
    if (this.month > otherDay.month) {
        return true;
    }
    return this.day > otherDay.day;
}

Day.prototype.greaterThanOrEqualTo = function(otherDay) {
    return  otherDay != undefined &&
            this.greaterThan(otherDay) ||
            this.equalTo(otherDay);
}

Day.prototype.equalTo = function(otherDay) {
    return  otherDay != undefined &&
            this.month === otherDay.month &&
            this.day === otherDay.day &&
            this.year === otherDay.year
}

Day.prototype.lessThan = function(otherDay) {
    if (!otherDay) return false;
    if (this.year > otherDay.year) {
        return false;
    }
    if (this.year < otherDay.year) {
        return true;
    }
    if (this.month > otherDay.month) {
        return false;
    }
    if (this.month < otherDay.month) {
        return true;
    }
    return this.day < otherDay.day;

}

Day.prototype.lessThanOrEqualTo = function(otherDay) {
    return this.lessThan(otherDay) ||
            this.equalTo(otherDay);
}

function displayMessage(message) {

}

function dayChanged() {
    highlightDivs();
}

function highlightDivs() {
    let start = getStart();
    let end = getEnd();
    let divs = document.querySelectorAll('.day');
    let month = getMonth();
    let year = getYear();
    for (let div of divs) {
        let val = parseInt(div.innerHTML);
        let day = new Day(month, val, year);
        if (day.equalTo(start)) {
            ensureClass(div, 'highlighted');
        } else if (day.greaterThanOrEqualTo(start) &&
                    day.lessThanOrEqualTo(end)){
            ensureClass(div, 'highlighted');
        } else {
            ensureNoClass(div, 'highlighted');
        }
    }
}

function ensureClass(el, className) {
    let fullClass = el.getAttribute('class')
    let currentClasses = fullClass.split(' ');
    if (currentClasses.indexOf(className) > -1) return;
    currentClasses.push(className);
    el.setAttribute('class', currentClasses.join(' '));
}

function ensureNoClass(el, className) {
    let fullClass = el.getAttribute('class');
    let currentClasses = fullClass.split(' ');
    let targetIndex = currentClasses.indexOf(className)
    if (targetIndex < 0) return;
    currentClasses.splice(targetIndex, 1);
    el.setAttribute('class', currentClasses.join(' '));
}

function changeMonth(event) {
    event.preventDefault();
    let button = event.currentTarget;
    let id = button.getAttribute('id');
    getNewMonth(id == 'next-month')
        .then(res => {
            updateMonth(res);
        })
        .catch(e => console.error(e));
}

function getNewMonth(next) {
    let query;
    let month = parseInt(getMonth());
    let year = parseInt(getYear());
    if (next) {
        let nextData = nextMonth(month, year);
        updateUrl(...nextData)
        return goToMonth(...nextData);
    }
    let lastData = lastMonth(month, year);
    updateUrl(...lastData);
    return goToMonth(...lastData);
}

function goToMonth(month, year) {
    updateStoredData(month, year);
    let query = getQuery(month, year);
    return get(`/calendar${query}`);
}

function updateStoredData(newMonth, newYear) {
    setMonth(newMonth);
    if (newYear) {
        setYear(newYear);
    }
}

function updateUrl(month, year) {
    window.history.pushState({month: month, year: year}, '', `/new?month=${month}&year=${year}`)
}

function getQuery(month, year) {
    return `?month=${month}&year=${year}`;
}

function nextMonth(month, year) {
    if (month >= 12) {
        return [1, year + 1]
    }
    return [month + 1, year];
}

function lastMonth(month, year) {
    if (month <= 1) {
        return [12, year -1];
    }
    return [month - 1, year]
}

function updateMonth(month) {
    updateInputs(month.month_number, month.year_number);
    updateDays(month.days);
    updateTitle(month);
}

function updateTitle(month) {
    let lastButton = document.querySelector('#last-month');
    let header = document.querySelector('.title-text');
    let nextButton = document.querySelector('#next-month');
    updateElementText(lastButton, month.last_month.name);
    updateElementText(header, `${month.this_month.name} ${month.this_month.year}`);
    updateElementText(nextButton, month.next_month.name);
}

function updateElementText(el, newText) {
    el.removeChild(el.lastChild);
    el.appendChild(document.createTextNode(newText));
}

function updateInputs(month, year) {
    let monthInput = document.querySelector('#month');
    if (monthInput)
        monthInput.setAttribute('value', month);
    let yearInput = document.querySelector('#year');
    if (yearInput)
        yearInput.setAttribute('value', year);
}

function updateDays(days) {
    let cal = document.querySelector('.calendar-body');
    removeDays(cal);
    addDays(cal, days)
}

function removeDays(cal) {
    while (cal.hasChildNodes()) {
        let lastChild = cal.lastElementChild;
        if (lastChild.getAttribute('class').indexOf('day-header') >  -1)
            break;
        cal.removeChild(lastChild)
    }
}

function addDays(cal, days) {
    for (let day of days) {
        cal.appendChild(dayDiv(day));
    }
}

function dayDiv(day) {
    let div = document.createElement('div');
    let dayClass = day.day ? 'day' : 'empty-day';
    let dow = getDow(day.dow);
    div.setAttribute('class', `${dayClass} ${dow}`);
    div.appendChild(document.createTextNode(day.day || ''));
    div.addEventListener('click', dayClicked);
    return div;
}

function getDow(num) {
    switch (num) {
        case 0:
            return 'sun';
        case 1:
            return 'mon';
        case 2:
            return 'tue';
        case 3:
            return 'wed';
        case 4:
            return 'thur';
        case 5:
            return 'fri';
        case 6:
            return 'sat';
    }
}

function get(url) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.addEventListener('readystatechange', (event) => {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                try {
                    resolve(JSON.parse(xhr.responseText));
                } catch (e) {
                    reject(e);
                }
            }
        });
        xhr.send();
    });
}