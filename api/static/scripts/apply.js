function toggle_email() {
    let email = document.getElementById('email');
    let append = document.getElementById('email_append');
    let addon = document.getElementById('email_addon');
    let help = document.getElementById('email_help');
    let val = document.getElementById('unt_student').value;

    let new_style = "";
    if (val == "No") {
        if (email != null) {
            email.remove();
        }
        new_style = "display: none;";
    } else {
        if (email == null) {
            let newElement = document.createElement("input");
            newElement.name = "unt_email";
            newElement.id = "email";
            newElement.type = "text";
            newElement.setAttribute('class', 'form-control');
            newElement.placeholder = "UNT Email Address";
            newElement.ariaLabel = "UNT Email Address";
            newElement.setAttribute('aria-describedby', 'basic-addon2');
            newElement.pattern = "^[A-z]{2,99}[0-9]*$";
            let next = document.getElementById('email_append');
            next.parentElement.insertBefore(newElement, next);
        }
    }

    append.style = new_style;
    addon.style = new_style;
    help.style = new_style;

}

document.getElementById('unt_student').addEventListener('change', toggle_email);
