let filtered = new Array();
let curr_filters = new Map();

let isSupported = CSS.supports('position', 'fixed');
console.log(isSupported);
//isSupported = false; // set to false for testing

let opened_dropdown = null;

const options = {
  attributes: true
}

let stored_element = null;
let stored_parent = null;
let observers = new Array();

function callback(mutationList, observer) {
  mutationList.forEach(function(mutation) {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
      if (mutation.target.getAttribute('class').split(' ').includes("show")) {
        if (mutation.target.parentElement != document.body) {
            let curr = mutation.target;
            curr.style = "position: absolute; z-index: 1000000000";
            document.body.style = "overflow-x: clip; max-width: 100vw;";
            stored_element = curr;
            stored_parent = curr.parentElement;
            curr.children[1].style.display = "none";
            document.body.insertBefore(curr, document.body.firstElementChild);
            window.scrollTo(10, 10);
            var timer = null;
            window.addEventListener('scroll', function() {
                if(timer !== null) {
                    clearTimeout(timer);        
                }
                timer = setTimeout(function() {
                    window.scrollTo(0, 0);
                }, 150);

            }, { once: true });
        }
      } else {
        if (stored_element == mutation.target) {
            mutation.target.style = "";
            mutation.target.children[1].style.display = "inline-flex";
            stored_parent.appendChild(mutation.target);
            console.log("Appended",mutation.target,"to",stored_parent);
            stored_element = null;
            stored_parent = null;
            document.body.style = "";
        }
      }
    }
  })
}

window.addEventListener('load', function() {
    let filters = document.getElementsByClassName('filter-select');
    for (let i = 0; i < filters.length; i++) { // for each filter
        let options = new Set([]);
        let id = filters[i].id;
        let elements = document.getElementsByClassName(id);

        for (let j = 0; j < elements.length; j++) { // for each campaign
            options.add(elements[j].innerHTML.replace(id.replaceAll('_',' ') + ': ','')); // add the associated value
            filtered.push(new Array()) // add empty array to filtered to maintain index
        }

        options = Array.from(options);
        options.sort()

        for (const option of options) {
            let newElement = document.createElement('option');
            newElement.innerHTML = option;
            newElement.value = option;
            newElement.setAttribute('onclick','filter(this);');
            filters[i].appendChild(newElement);
        }
    }
    $('select').selectpicker();

    // add event listeners if unsupported position static
    if (!isSupported) {
        let elements = document.getElementsByClassName('bootstrap-select');
        for (let i = 0; i < elements.length; i++) {
            observers.push(new MutationObserver(callback));
            observers[i].observe(elements[i], options)
        }
    }

    // expand button event listeners
    let expand_buttons = document.getElementsByClassName('expand_button');
    for (let i = 0; i < expand_buttons.length; i++) {
        expand_buttons[i].addEventListener('click', function(event) {
            let element = event.target || event.srcElement;
            expand(element);
        });
    }

});

function getSelectValues(select) { // https://stackoverflow.com/questions/5866169/how-to-get-all-selected-values-of-a-multiple-select-box
    var result = [];
    var options = select && select.options;
    var opt;
  
    for (var i=0, iLen=options.length; i<iLen; i++) {
      opt = options[i];
  
      if (opt.selected) {
        result.push(opt.value || opt.text);
      }
    }
    return result;
  }

function filter(element) {

    let id = element.id;
    let values = getSelectValues(element);
    let elements = document.getElementsByClassName(id); // everything we need to check

    if (curr_filters.has(id)) { // id has already been stored
        unfilter(null, id); // unset
    }
    if (values.length == 0) {
        return;
    }
    curr_filters.set(id, values);

    for (let i = 0; i < elements.length; i++) { // for each campaign
        let curr = elements[i].innerHTML.replace(id.replaceAll('_',' ') + ': ','');
        let index = curr_filters.get(id).indexOf(curr);
        if (index == -1) { // not found in list of allowed items
            elements[i].parentElement.parentElement.style = "display: none;";
            let index = filtered[i].indexOf(id); // check if already filtered due to this
            if (index == -1) { // if not found
                filtered[i].push(id); // add to filtered list
            }
        }
    }

}

function unfilter(element, id = null) {
    if (id == null) {
        id = element.parentElement.id;
    }
    
    let elements = document.getElementsByClassName(id);

    if (curr_filters.has(id)) { // if found
        curr_filters.delete(id); // remove from filter list
    }

    for (let i = 0; i < elements.length; i++) { // for each campaign
        let index = filtered[i].indexOf(id);
        if (index !== -1) {
            filtered[i].splice(index, 1);
            if (filtered[i].length == 0) {
                elements[i].parentElement.parentElement.style = "";
            } else {
            }
        }
    }
}

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

