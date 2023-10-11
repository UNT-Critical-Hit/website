function toggle_email(on = False) {

    let email = document.getElementById('email');
    let append = document.getElementById('email_append');
    let addon = document.getElementById('email_addon');
    let help = document.getElementById('email_help');

    let new_style = "";
    if (!on) {
        new_style = "display: none;";
    }

    email.style = new_style;
    append.style = new_style;
    addon.style = new_style;
    help.style = new_style;

}