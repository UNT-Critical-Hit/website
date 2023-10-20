// global list of campaigns and what filters they don't match, remove from nested list when filter is removed, if nested list is empty add campaign back in
let filtered = new Array();
let curr_filters = new Array();

window.addEventListener('load', function() {
    let filters = document.getElementsByClassName('filter-select');
    for (let i = 0; i < filters.length; i++) {
        let options = new Set([]);
        let id = filters[i].id;
        let elements = document.getElementsByClassName(id);

        for (let j = 0; j < elements.length; j++) { // for each campaign
            options.add(elements[j].innerHTML.replace(id.replace('_',' ') + ': ','')); // add the associated value
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
});

function filter(element) {
    let id = element.parentElement.id;
    let value = element.value;
    let elements = document.getElementsByClassName(id); // everything we need to check

    let index = curr_filters.indexOf(id);
    if (index == -1) { // if not found
        curr_filters.push(id); // add to filtered list
    } else {
        unfilter(null, id); // unfilter the entries
        curr_filters.push(id); // add to filtered list
    }

    for (let i = 0; i < elements.length; i++) { // for each campaign
        if (elements[i].innerHTML.replace(id.replace('_',' ') + ': ','') != value) {
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

    console.log("Unfiltering for",id);
    
    let elements = document.getElementsByClassName(id);

    let index = curr_filters.indexOf(id);
    if (index !== -1) { // if found
        curr_filters.splice(index, 1); // remove from filtered list
    }

    for (let i = 0; i < elements.length; i++) { // for each campaign
        let index = filtered[i].indexOf(id);
        if (index !== -1) {
            //console.log("Before removing",id,": ",filtered[i]);
            filtered[i].splice(index, 1);
            //console.log("After: ",filtered[i],"\n\n\n");
            if (filtered[i].length == 0) {
                //console.log("Brought back",elements[i].parentElement.parentElement);
                elements[i].parentElement.parentElement.style = "";
            } else {
                console.log("Didn't remove since length is",filtered[i].length,":",elements[i].parentElement.parentElement," | ",filtered[i]);
            }
        }
    }
    console.log("\n\n\n\n\n\n");
}