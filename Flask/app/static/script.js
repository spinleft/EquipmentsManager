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

function deleteRecord(index, name, model, id) {
    var form = document.getElementById("delete-" + index);
    if (confirm("是否删除：" + name + " " + model + " " + id + "？")) {
        var file = document.getElementById("contract-file-" + index);
        var photo = document.getElementById("photo-" + index);
        var locationPhoto = document.getElementById("location-photo-" + index);
        if (file.innerHTML.indexOf('None') == -1 || photo.innerHTML != 'None' || locationPhoto.innerHTML != 'None') {
            if (confirm("是否删除文件、照片等数据？")) {
                document.getElementById("delete-file-" + index).value = "true";
            }
            else {
                document.getElementById("delete-file-" + index).value = "false";
            }
        }
        return true;
    }
    else
        return false;
}
