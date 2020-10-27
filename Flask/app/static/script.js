function deleteRecord(name, model, id) {
    alert(name + " " + model + " " + id)
}

function displaySelectBox() {
    var p = document.getElementById("select-tag")
    var box = document.getElementById("select-box");
    var display = window.getComputedStyle(box).display;
    if (display == 'none') {
        p.innerHTML = "-筛选"
        box.style.display = 'block';
    }
    else {
        p.innerHTML = "+筛选"
        box.style.display = 'none';
    }
}

function displayInsertBox() {
    var p = document.getElementById("insert-tag")
    var box = document.getElementById("insert-box");
    var display = window.getComputedStyle(box).display;
    if (display == 'none') {
        p.innerHTML = "-插入"
        box.style.display = 'block';
    }
    else {
        p.innerHTML = "+插入"
        box.style.display = 'none';
    }
}

var attachname = "合同文件";
var i = 1;
function addInput() {
    if (i > 0) {
        var attach = attachname + i;
        if (createInput(attach))
            i = i + 1;
    }
}

function deleteInput() {
    if (i > 1) {
        i = i - 1;
        if (!removeInput())
            i = i + 1;
    }
}

function createInput(name) {
    // var aElement = document.createElement("input");
    // aElement.name = nm;
    // aElement.id = nm;
    // aElement.type = "file";
    // aElement.size = "50";
    // if (document.getElementById("upload-contract-file").appendChild(aElement) == null)
    //     return false;
    // return true;
    var aItem = document.createElement("li");
    aItem.id = "upload-contract-file-li-" + name;
    var aElement = document.createElement("input");
    aElement.name = name;
    aElement.id = "upload-contract-file-" + name;
    aElement.type = "file";
    aElement.size = "50";
    if (document.getElementById("upload-contract-file").appendChild(aItem) == null)
        return false;
    else {
        document.getElementById("upload-contract-file-li-" + name).append(aElement);
        return true;
    }
}
function removeInput() {
    var aList = document.getElementById("upload-contract-file");
    if (aList.removeChild(aList.lastChild) == null)
        return false;
    return true;
}