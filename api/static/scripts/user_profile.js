window.addEventListener('load', function() {

    let unt_student = document.getElementById('user_unt_student').value;
    if (unt_student == "True") {
        document.getElementById('unt_student_yes').setAttribute('selected', true);
    } else if(unt_student == "False") {
        document.getElementById('unt_student_no').setAttribute('selected', false);
        toggle_email(false);
    }

    let alert_card = document.getElementById('alert_card');

    let updated = document.getElementById('updated');
    if (document.getElementById('alert_card_message').innerHTML) {
        alert_card.style.display = "";
    }
    document.getElementById('close_card').addEventListener('click', function() {
        alert_card.remove();
    });

});