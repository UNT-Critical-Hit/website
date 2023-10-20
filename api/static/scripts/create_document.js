function add_section(element) {
    let newElement = document.createElement('div');
    newElement.className = "mb-3";
    newElement.innerHTML = "<h5><input class=\"form-control\" placeholder=\"Section Name\"></h5>" +
    "<button onclick=\"add_field(this)\" type=\"button\" class=\"btn btn-primary\">Add field</button>";
    element.parentElement.insertBefore(newElement, element);
}

function add_field(element) {
    let newElement = document.createElement('div');
    newElement.className = "mb-3";
    newElement.innerHTML = "<div class=\"input-group\">" +
    "<button onclick=\"add_field(this)\" type=\"button\" class=\"btn btn-primary\">Add field</button>";
    element.parentElement.insertBefore(newElement, element);
}