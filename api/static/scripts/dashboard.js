window.addEventListener('load', function() {

    // expand button event listeners
    let expand_buttons = document.getElementsByClassName('expand_button');
    for (let i = 0; i < expand_buttons.length; i++) {
        expand_buttons[i].addEventListener('click', function(event) {
            let element = event.target || event.srcElement;
            expand(element);
        });
    }

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

