function toggle_other(on = false) {
    let element = document.getElementById('other');
    let new_style = "";
    if (!on) {
        new_style = "display: none;";
        element.required = false;
    } else {
        element.required = true;
    }
    element.style = new_style;
}

function toggle_inperson(on = false) {
    let element = document.getElementById('inperson_location');
    let new_style = "";
    if (!on) {
        new_style = "display: none;";
        element.required = false;
    } else {
        element.required = true;
    }
    element.style = new_style;
    toggle_other();
}

function toggle_system_other(on = false) {
    let element = document.getElementById('other_system');
    let new_style = "";
    if (!on) {
        new_style = "display: none;";
        element.required = false;
    } else {
        element.required = true;
    }
    element.style = new_style;
    toggle_other();
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
    element = document.getElementById('playstyle');
    label = document.getElementById('playstyle_label');
    if (on) {
        element.required = true;
        element.style = "";
        label.style = "";
    } else {
        element.required = false;
        element.style = "display: none;";
        label.style = "display: none;";
    }
}

function toggle_date(on = false) {
    let date = document.getElementById('date');
    let date_append = document.getElementById('date_append');
    let day = document.getElementById('day');
    let day_append = document.getElementById('day_append');

    if (on) {
        date.required = true;
        date.style = "";
        date_append.style = "";
        day.required = true;
        day.style = "display: none;";
        day_append.style = "display: none;";
    } else {
        date.required = false;
        date.style = "display: none;";
        date_append.style = "display: none;";
        day.required = false;
        day.style = "";
        day_append.style = "";
    }
}

window.addEventListener('load', function() {
    validate_desc();
    validate_max();
    validate_min();
    validate_playstyle();
});