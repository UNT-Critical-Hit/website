let filtered = new Array();
let curr_filters = new Map();

window.addEventListener('load', function() {
    let filters = document.getElementsByClassName('filter-select');
    for (let i = 0; i < filters.length; i++) {
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
                console.log("Brought back since length is 0");
                console.log(elements[i].parentElement.parentElement);
                elements[i].parentElement.parentElement.style = "";
            } else {
                console.log("Didn't remove since length is > 0:",filtered[i]);
            }
        } else {
            console.log("Could not find",id,"in",filtered[i]);
            if (filtered[i].length > 0) {
                console.log("^ Actually, filtered[i][0] is",filtered[i][0])
            }
        }
    }
}