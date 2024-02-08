window.addEventListener('load', function() {

    // expand button event listeners
    let expand_buttons = document.getElementsByClassName('expand_button');
    for (let i = 0; i < expand_buttons.length; i++) {
        expand_buttons[i].addEventListener('click', function(event) {
            let element = event.target || event.srcElement;
            expand(element);
        });
    }

    // alert card event listeners
    let alert_card = document.getElementById('alert_card');
    document.getElementById('close_card').addEventListener('click', function() {
        alert_card.remove();
    });

});

let expanded = null;

function expand(element) {
    if (element.innerHTML == 'Expand') {
        if (expanded != null) {
            expanded.innerHTML = 'Expand';
            expanded.parentElement.parentElement.setAttribute('class', 'card campaign-card');
        }
        element.innerHTML = 'Revert';
        element.parentElement.parentElement.setAttribute('class', 'card campaign-card campaign-card-expanded');
        expanded = element;
    } else {
        element.innerHTML = 'Expand';
        element.parentElement.parentElement.setAttribute('class', 'card campaign-card');
    }
}

