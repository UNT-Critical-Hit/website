function toggle_other(on = false) {
    let element = document.getElementById('other');
    if (!on) {
        if (element != null) {
            element.remove();
        }
    } else {
        if (element == null) {
            let newElement = document.createElement('input');
            newElement.name = "location_inperson_other";
            newElement.id = "other";
            newElement.type = "text";
            newElement.setAttribute('class', 'form-control');
            newElement.placeholder = "Other...";
            newElement.ariaLabel = "Other";
            newElement.setAttribute('aria-describedby', 'other_append');
            newElement.pattern = "^[A-z]{2,99}[0-9]*$";
            newElement.required = true;
            let next = document.getElementById('after_location_inperson_other');
            next.parentElement.insertBefore(newElement, next);
        }
    }
}

function toggle_inperson(on = false) {
    let element = document.getElementById('inperson_location');
    if (!on) {
        if (element != null) {
            element.remove();
        }
    } else {
        if (element == null) {
            let newElement = document.createElement('div');
            newElement.id = "location_inperson_div"
            newElement.innerHTML = "<select name=\"location_inperson\" required class=\"custom-select\" id=\"inperson_location\" autocomplete=\"off\">" +
            "<option value=\"\" onclick=\"toggle_other();\" selected>Where on-campus will sessions be held?</option>" +
            "<option value=\"Willis Library\" onclick=\"toggle_other();\">Willis Library</option>" +
            "<option value=\"Media Library\" onclick=\"toggle_other();\">Media Library</option>" +
            "<option value=\"Sycamore Library\" onclick=\"toggle_other();\">Sycamore Library</option>" +
            "<option value=\"Other\" onclick=\"toggle_other(true);\">Other</option>" +
            "</select>";
            let next = document.getElementById('after_location_inperson_div');
            next.parentElement.insertBefore(newElement, next);
        }
    }
    toggle_other();
}

function toggle_system_other(on = false) {
    let element = document.getElementById('other_system');
    if (!on) {
        if (element != null) {
            element.remove();
        }
    } else {
        if (element == null) {
            let newElement = document.createElement('input');
            newElement.name = "system_other";
            newElement.id = "other_system";
            newElement.type = "text";
            newElement.setAttribute('class', 'form-control');
            newElement.placeholder = "Other...";
            newElement.ariaLabel = "Other";
            newElement.setAttribute('aria-describedby','other_append');
            newElement.pattern = "^[A-z]{2,99}[0-9]*$";
            newElement.required = true;
            let next = document.getElementById('after_system_other');
            next.parentElement.insertBefore(newElement, next);
        }
    }
    //toggle_other();
}

function validate_desc() {
    let element = document.getElementById('desc');
    let value = element.value;
    let invalid = true;

    if (value.length < 100 || !value) {
        element.setCustomValidity('Please type at least 100 characters');
    } else if (value.length > 600) {
        element.setCustomValidity('Please type no more than 600 characters');
    } else {
        invalid = false;
    }

    if (invalid == true) {
        element.setAttribute('class', 'form-control is-invalid');
    } else {
        element.setAttribute('class', 'form-control');
        element.setCustomValidity('');
    }
}

function validate_playstyle() {
    let element = document.getElementById('playstyle');
    let value = element.value;
    let invalid = true;

    if (value.length < 3 || !value) {
        element.setCustomValidity('Please type at least 3 characters');
    } else if (value.length > 200) {
        element.setCustomValidity('Please type no more than 200 characters');
    } else {
        invalid = false;
    }

    if (invalid == true) {
        element.setAttribute('class', 'form-control is-invalid');
    } else {
        element.setAttribute('class', 'form-control');
        element.setCustomValidity('');
    }
}

function validate_min() {
    let element = document.getElementById('min_players');
    let max = Number(document.getElementById('max_players').value);
    let value = Number(element.value);
    let invalid = true;

    if (value < 1) {
        element.setCustomValidity('Minimum players must be greater than zero');
    } else if (value > max) {
        element.setCustomValidity('Minimum players cannot be greater than maximum players');
    } else {
        invalid = false;
    }

    if (invalid == true) {
        element.isvalid = false;
    } else {
        element.isvalid = true;
        element.setCustomValidity('');
    }
}

function validate_max() {
    let element = document.getElementById('max_players');
    let min = Number(document.getElementById('min_players').value);
    let value = Number(element.value);
    let invalid = true;

    if (value < 1) {
        element.setCustomValidity('Maximum players must be greater than zero');
    } else if (value < min) {
        element.setCustomValidity('Maximum players cannot be less than minimum players');
    } else {
        invalid = false;
    }

    if (invalid == true) {
        element.isvalid = false;
    } else {
        element.isvalid = true;
        element.setCustomValidity('');
    }
}

function toggle_playstyle(on = false) {

    let element = document.getElementById('playstyle_div');
    if (on == true) {
        if (element == null) {
            let newElement = document.createElement('div');
            newElement.id = "playstyle_div";
            newElement.innerHTML = "<label for=\"playstyle\">DM Playstyle</label>" +
            "<textarea name=\"playstyle\" id=\"playstyle\" class=\"form-control\" oninput=\"validate_playstyle()\" placeholder=\"Please describe your playstle as a DM briefly.\" required></textarea>"
            let next = document.getElementById('after_playstyle');
            next.parentElement.insertBefore(newElement, next);
            validate_playstyle();
        }
    } else {
        if (element != null) {
            element.remove();
        }
    }
    
}

function toggle_date(on = false) {
    let date = document.getElementById('date');
    let date_append = document.getElementById('date_append');
    let day = document.getElementById('day');
    let day_append = document.getElementById('day_append');

    if (on == true) {
        if (date == null) {
            let newDate = document.createElement('input'); // <input name="date" id="date" type="date" class="form-control" style="display: none;"></input>
            newDate.name = "date";
            newDate.id = "date";
            newDate.type = "date";
            newDate.required = true;
            newDate.setAttribute('class', 'form-control');
            let afterDate = document.getElementById('after_date');
            afterDate.parentElement.insertBefore(newDate, afterDate);
        }
        date_append.style = "";
        if (day != null) {
            day.remove();
        }
        day_append.style = "display: none;";
    } else {
        if (date != null) {
            date.remove();
        }
        date_append.style = "display: none;";
        if (day == null) {
            let newDay = document.createElement('select');
            newDay.name = "day";
            newDay.id = "day";
            newDay.required = true;
            newDay.setAttribute('class', 'custom-select');
            newDay.innerHTML = "<option value=\"\" selected>Weekday</option>" +
            "<option value=\"Sunday\">Sunday</option>" +
            "<option value=\"Monday\">Monday</option>" +
            "<option value=\"Tuesday\">Tuesday</option>" +
            "<option value=\"Wednesday\">Wednesday</option>" +
            "<option value=\"Wednesday\">Thursday</option>" +
            "<option value=\"Friday\">Friday</option>" +
            "<option value=\"Saturday\">Saturday</option>"
            let afterDay = document.getElementById('after_day');
            afterDay.parentElement.insertBefore(newDay, afterDay);
        }
        day_append.style = "";
    }
}

window.addEventListener('load', function() {
    validate_desc();
    validate_max();
    validate_min();
    //validate_playstyle();
});