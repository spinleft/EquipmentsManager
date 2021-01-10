function initPage() {
    statusTds = document.getElementsByClassName("info-status");
    for (var i = 0; i < statusTds.length; i++) {
        switch (statusTds[i].innerHTML) {
            case "在用":
                statusTds[i].style.backgroundColor = "green";
                break;
            case "待用":
                statusTds[i].style.backgroundColor = "gray";
                break;
            case "被借":
                statusTds[i].style.backgroundColor = "yellow";
                break;
            case "待维修":
                statusTds[i].style.backgroundColor = "red";
                break;
            case "维修中":
                statusTds[i].style.backgroundColor = "orange";
                break;
            default:
                break;
        }
    }
}

function displayDetailsForm() {
    var type = document.getElementById("details-type").innerHTML
    if (type == "材料") {
        document.getElementById("details-type-a").selected = true;
        document.getElementById("details-type-b").selected = false;
    } else {
        document.getElementById("details-type-a").selected = false;
        document.getElementById("details-type-b").selected = true;
    }
    var status = document.getElementById("details-status").innerHTML;
    switch (status) {
        case "在用":
            document.getElementById("details-status-a").selected = true;
            break;
        case "待用":
            document.getElementById("details-status-b").selected = true;
            break;
        case "被借":
            document.getElementById("details-status-c").selected = true;
            break;
        case "待维修":
            document.getElementById("details-status-d").selected = true;
            break;
        case "维修中":
            document.getElementById("details-status-e").selected = true;
            break;
        default:
            document.getElementById("details-status-a").selected = true;
    }
    var show = document.getElementsByClassName("details-show")
    var hide = document.getElementsByClassName("details-hide")
    for (var i = 0; i < show.length; i++) {
        show[i].style.display = "none";
    }
    for (var i = 0; i < hide.length; i++) {
        hide[i].style.display = "block";
    }
    var showButton = document.getElementsByClassName("details-show-button")
    var hideButton = document.getElementsByClassName("details-hide-button")
    for (var i = 0; i < showButton.length; i++) {
        showButton[i].style.display = "none";
    }
    for (var i = 0; i < hideButton.length; i++) {
        hideButton[i].style.display = "inline";
    }
    return;
}

function hideDetailsForm() {
    var show = document.getElementsByClassName("details-show")
    var hide = document.getElementsByClassName("details-hide")
    for (var i = 0; i < show.length; i++) {
        show[i].style.display = "block";
    }
    for (var i = 0; i < hide.length; i++) {
        hide[i].style.display = "none";
    }
    var showButton = document.getElementsByClassName("details-show-button")
    var hideButton = document.getElementsByClassName("details-hide-button")
    for (var i = 0; i < showButton.length; i++) {
        showButton[i].style.display = "inline";
    }
    for (var i = 0; i < hideButton.length; i++) {
        hideButton[i].style.display = "none";
    }
    return 0;
}

function createInputFile() {
    var index = document.getElementsByClassName("upload-contract-file-item").length;
    var newInputFile = document.createElement("input");
    newInputFile.id = "contract-file-" + index.toString();
    newInputFile.name = "contract_file_" + index;
    newInputFile.type = "file";
    newInputFile.size = "50";
    newInputFile.style.display = "none";
    var func = function(obj) {
        return function() {
            addInputFile(obj);
        };
    };
    newInputFile.addEventListener("change", func(newInputFile));
    newInputFile.click();
    return false;
}

function addInputFile(newInputFile) {
    var index = document.getElementsByClassName("upload-contract-file-item").length;
    var filepath = newInputFile.value.split('\\');
    var filename = filepath[filepath.length - 1];
    var newItem = document.createElement("li");
    newItem.id = "upload-contract-file-item-" + index.toString();
    newItem.className = "upload-contract-file-item";
    var newSpan = document.createElement("span");
    newSpan.innerHTML = filename;
    var newInputText = document.createElement("input");
    newInputText.id = "contract-filename-" + index.toString();
    newInputText.type = "text";
    newInputText.name = "contract_filename_" + index.toString();
    newInputText.value = filename;
    newInputText.style.display = "none";
    var newInputButton = document.createElement("input");
    newInputButton.type = "button";
    newInputButton.value = "删除";
    var func = function(index) {
        return function() {
            deleteFile(index);
        };
    };
    newInputButton.addEventListener("click", func(index.toString()));
    newItem.appendChild(newSpan);
    newItem.appendChild(newInputText);
    newItem.appendChild(newInputFile);
    newItem.appendChild(newInputButton);
    document.getElementById("upload-contract-file").appendChild(newItem);
    return;
}

function deleteFile(index) {
    var itemId = "upload-contract-file-item-" + index.toString();
    var ulNode = document.getElementById("upload-contract-file");
    var liNode = document.getElementById(itemId);
    ulNode.removeChild(liNode);
    sortFileItems();
    return;
}

function sortFileItems() {
    var liItems = document.getElementsByClassName("upload-contract-file-item");
    var func = function(index) {
        return function() {
            deleteFile(index);
        };
    };
    for (var i = 0; i < liItems.length; i++) {
        var oldId = liItems[i].id.split('-');
        var oldIndex = oldId[oldId.length - 1];
        liItems[i].id = "upload-contract-file-item-" + i.toString();
        var filename = document.getElementById("contract-filename-" + oldIndex);
        filename.id = "contract-filename-" + i.toString();
        filename.name = "contract_filename_" + i.toString();
        var file = document.getElementById("contract-file-" + oldIndex);
        if (file) {
            file.id = "contract-file-" + i.toString();
            file.name = "contract_file_" + i.toString();
        }
        var deleteButton = document.getElementById("delete-contract-file-button-" + oldIndex)
        liItems[i].removeChild(deleteButton);
        var newInputButton = document.createElement("input");
        newInputButton.type = "button";
        newInputButton.value = "删除";
        newInputButton.addEventListener("click", func(i.toString()));
        liItems[i].appendChild(newInputButton);
    }
    return;
}

function createInputPhoto() {
    var index = document.getElementsByClassName("upload-photo-item").length;
    var newInputFile = document.createElement("input");
    newInputFile.id = "photo-" + index.toString();
    newInputFile.name = "photo_" + index.toString();
    newInputFile.type = "file";
    newInputFile.size = "50";
    newInputFile.style.display = "none";
    var func = function(obj) {
        return function() {
            addInputPhoto(obj);
        };
    };
    newInputFile.addEventListener("change", func(newInputFile));
    newInputFile.click();
    return false;
}

function addInputPhoto(newInputFile) {
    var index = document.getElementsByClassName("upload-photo-item").length;
    var filepath = newInputFile.value.split('\\');
    var filename = filepath[filepath.length - 1];
    var newItem = document.createElement("li");
    newItem.id = "upload-photo-item-" + index.toString();
    newItem.className = "upload-photo-item";
    var newSpan = document.createElement("span");
    newSpan.innerHTML = filename;
    var newInputText = document.createElement("input");
    newInputText.id = "photoname-" + index.toString();
    newInputText.type = "text";
    newInputText.name = "photoname_" + index.toString();
    newInputText.value = filename;
    newInputText.style.display = "none";
    var newInputButton = document.createElement("input");
    newInputButton.type = "button";
    newInputButton.value = "删除";
    var func = function(index) {
        return function() {
            deletePhoto(index);
        };
    };
    newInputButton.addEventListener("click", func(index.toString()));
    newItem.appendChild(newSpan);
    newItem.appendChild(newInputText);
    newItem.appendChild(newInputFile);
    newItem.appendChild(newInputButton);
    document.getElementById("upload-photo").appendChild(newItem);
    return;
}

function deletePhoto(index) {
    var itemId = "upload-photo-item-" + index.toString();
    var ulNode = document.getElementById("upload-photo");
    var liNode = document.getElementById(itemId);
    ulNode.removeChild(liNode);
    sortPhotoItems();
    return;
}

function sortPhotoItems() {
    var liItems = document.getElementsByClassName("upload-photo-item");
    var func = function(index) {
        return function() {
            deletePhoto(index);
        };
    };
    for (var i = 0; i < liItems.length; i++) {
        var oldId = liItems[i].id.split('-');
        var oldIndex = oldId[oldId.length - 1];
        liItems[i].id = "upload-photo-item-" + i.toString();
        var photoname = document.getElementById("photoname-" + oldIndex);
        photoname.id = "photoname-" + i.toString();
        photoname.name = "photoname_" + i.toString();
        var photo = document.getElementById("photo-" + oldIndex);
        if (photo) {
            photo.id = "photo-" + i.toString();
            photo.name = "photo_" + i.toString();
        }
        var deleteButton = document.getElementById("delete-photo-button-" + oldIndex)
        liItems[i].removeChild(deleteButton);
        var newInputButton = document.createElement("input");
        newInputButton.type = "button";
        newInputButton.value = "删除";
        newInputButton.addEventListener("click", func(i.toString()));
        liItems[i].appendChild(newInputButton);
    }
    return;
}

function createInputLocationPhoto() {
    var index = document.getElementsByClassName("upload-location-photo-item").length;
    var newInputFile = document.createElement("input");
    newInputFile.id = "location-photo-" + index.toString();
    newInputFile.name = "location_photo_" + index.toString();
    newInputFile.type = "file";
    newInputFile.size = "50";
    newInputFile.style.display = "none";
    var func = function(obj) {
        return function() {
            addInputLocationPhoto(obj);
        };
    };
    newInputFile.addEventListener("change", func(newInputFile));
    newInputFile.click();
    return false;
}

function addInputLocationPhoto(newInputFile) {
    var index = document.getElementsByClassName("upload-location-photo-item").length;
    var filepath = newInputFile.value.split('\\');
    var filename = filepath[filepath.length - 1];
    var newItem = document.createElement("li");
    newItem.id = "upload-location-photo-item-" + index.toString();
    newItem.className = "upload-location-photo-item";
    var newSpan = document.createElement("span");
    newSpan.innerHTML = filename;
    var newInputText = document.createElement("input");
    newInputText.id = "location-photoname-" + index.toString();
    newInputText.type = "text";
    newInputText.name = "location_photoname_" + index;
    newInputText.value = filename;
    newInputText.style.display = "none";
    var newInputButton = document.createElement("input");
    newInputButton.type = "button";
    newInputButton.value = "删除";
    var func = function(index) {
        return function() {
            deleteFile(index);
        };
    };
    newInputButton.addEventListener("click", func(index.toString()));
    newItem.appendChild(newSpan);
    newItem.appendChild(newInputText);
    newItem.appendChild(newInputFile);
    newItem.appendChild(newInputButton);
    document.getElementById("upload-location-photo").appendChild(newItem);
    return;
}

function deleteLocationPhoto(index) {
    var itemId = "upload-location-photo-item-" + index.toString();
    var ulNode = document.getElementById("upload-location-photo");
    var liNode = document.getElementById(itemId);
    ulNode.removeChild(liNode);
    sortLocationPhotoItems();
    return;
}

function sortLocationPhotoItems() {
    var liItems = document.getElementsByClassName("upload-location-photo-item");
    var func = function(index) {
        return function() {
            deleteLocationPhoto(index);
        };
    };
    for (var i = 0; i < liItems.length; i++) {
        var oldId = liItems[i].id.split('-');
        var oldIndex = oldId[oldId.length - 1];
        liItems[i].id = "upload-location-photo-item-" + i.toString();
        var photoname = document.getElementById("location-photoname-" + oldIndex);
        photoname.id = "location-photoname-" + i.toString();
        photoname.name = "location_photoname_" + i.toString();
        var photo = document.getElementById("location-photo-" + oldIndex);
        if (photo) {
            photo.id = "location-photo-" + i.toString();
            photo.name = "location_photo_" + i.toString();
        }
        var deleteButton = document.getElementById("delete-location-photo-button-" + oldIndex)
        liItems[i].removeChild(deleteButton);
        var newInputButton = document.createElement("input");
        newInputButton.type = "button";
        newInputButton.value = "删除";
        newInputButton.addEventListener("click", func(i.toString()));
        liItems[i].appendChild(newInputButton);
    }
    return;
}

function submitDetailsForm() {
    var detailsForm = document.getElementById("details");
    detailsForm.submit();
    return;
}

function confirmDelete(url) {
    if (window.confirm("确定删除吗？")) {
        window.location.assign(url);
        return true;
    } else {
        return false;
    }
}

function selectAllCols() {
    var checkBoxs = document.getElementsByClassName("info-select-col");
    for (var i = 0; i < checkBoxs.length; i++) {
        checkBoxs[i].checked = true;
    }
    var button = document.getElementById("info-select-all-cols");
    button.removeEventListener("click", selectAllCols);
    button.addEventListener("click", selectNoneCols);
    return;
}

function selectNoneCols() {
    var checkBoxs = document.getElementsByClassName("info-select-col");
    for (var i = 0; i < checkBoxs.length; i++) {
        checkBoxs[i].checked = false;
    }
    var button = document.getElementById("info-select-all-cols");
    button.removeEventListener("click", selectNoneCols);
    button.addEventListener("click", selectAllCols);
    return;
}

function selectAllRows() {
    var checkBoxs = document.getElementsByClassName("info-select-row");
    for (var i = 0; i < checkBoxs.length; i++) {
        checkBoxs[i].checked = true;
    }
    var button = document.getElementById("info-select-all-rows");
    button.removeEventListener("click", selectAllRows);
    button.addEventListener("click", selectNoneRows);
    return;
}

function selectNoneRows() {
    var checkBoxs = document.getElementsByClassName("info-select-row");
    for (var i = 0; i < checkBoxs.length; i++) {
        checkBoxs[i].checked = false;
    }
    var button = document.getElementById("info-select-all-rows");
    button.removeEventListener("click", selectNoneRows);
    button.addEventListener("click", selectAllRows);
    return;
}

function confirmMultiDelete() {
    var infoForm = document.getElementById("info-form");
    if (window.confirm("确定删除这些数据吗？")) {
        infoForm.submit();
        return true;
    } else {
        return false;
    }
}

function confirmMultiExport() {
    var url = document.getElementById("button-info-export").value;
    var infoForm = document.getElementById("info-form");
    infoForm.action = url;
    infoForm.submit();
    return;
}

function generateCompare(col) {
    return function(row1, row2) {
        var value1 = row1.cells[col].firstChild.nodeValue;
        var value2 = row2.cells[col].firstChild.nodeValue;
        return value1.localeCompare(value2, 'zh');
    }
}

function sortRows(col) {
    var oldTable = document.getElementById("info-table");
    var oldBody = oldTable.tBodies[0];
    var oldRows = oldBody.rows;
    var rowArray = new Array();
    for (var i = 0; i < oldRows.length; i++) {
        rowArray[i] = oldRows[i];
    }
    if (oldTable.sortCol == col) {
        rowArray.reverse();
    } else {
        rowArray.sort(generateCompare(col))
    }
    var newFragment = document.createDocumentFragment();
    for (var i = 0; i < rowArray.length; i++) {
        if (i % 2) {
            rowArray[i].className = "info-table-item-even";
        } else {
            rowArray[i].className = "info-table-item-odd";
        }
        newFragment.appendChild(rowArray[i]);
    }
    oldBody.appendChild(newFragment);
    oldTable.sortCol = col;
    return;
}