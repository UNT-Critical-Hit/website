let unt_student = document.getElementById('user_unt_student').value;
if (unt_student == "True") {
    document.getElementById('unt_student_yes').setAttribute('selected', true);
} else if(unt_student == "False") {
    document.getElementById('unt_student_no').setAttribute('selected', false);
    toggle_email(false);
}