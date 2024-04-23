var tagId = 1;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function deleteTag(id) {
    var row = document.getElementById("Tag" + id);
    if (row) {
        row.parentNode.removeChild(row);
        let s = `Tag${id}`;
    }
}


function saveNewTag(event) {
    event.preventDefault();

    var inputColor = document.getElementById("tagColor");
    var inputName = document.getElementById("tagName");

    var color = inputColor.value;
    var name = inputName.value;

    newRowInTable(tagId, name, color);
    tagId += 1;
}


function newRowInTable(id, name, color) {
    let table = document.getElementById("tabelTagBody");

    let row = table.insertRow(-1);
    row.id = "Tag" + id;
    let c1 = row.insertCell(0);
    let c2 = row.insertCell(1);
    let c3 = row.insertCell(2);
    c1.style = "text-align: center;";
    c2.style = "text-align: center;";
    c3.style = "text-align: center;";

    let box = `<input type="text" id="Tag${id}Name" value="${name}">`;
    c1.innerHTML = box;

    box = `<input type="color" id="Tag${id}Color" value="${color}">`;
    c2.innerHTML = box;

    box = `<span style="cursor: pointer; margin-right: 5px; color: red;" onclick="deleteTag(${id})">❌</span>`;
    c3.innerHTML = box;
}


function uploadProject() {
    var formData = new FormData();

    var images_file = document.getElementById('fileInput').files;
    for (var i = 0; i < images_file.length; i++) {
        formData.append('images', images_file[i]);
    }

    var nameProject = document.getElementById('projectName').value;

    if (images_file.length === 0 || nameProject.trim() === '') {
        alert('Заполните все формы');
        return;
    }
    var images = Array.from(images_file)

    var tags = [];

    // Получаем таблицу тегов
    var table = document.getElementById('tabelTagBody');

    // Проходим по каждой строке таблицы
    for (var i = 0; i < table.rows.length; i++) {
        // Получаем ячейки в текущей строке
        var cells = table.rows[i].cells;

        // Получаем значения названия и цвета тега из ячеек
        var tagName = cells[0].querySelector('input[type="text"]').value;
        var tagColor = cells[1].querySelector('input[type="color"]').value;

        if (tagName.trim() === '' || tagColor.trim() === '') {
            alert('Заполните все формы');
            return;
        }

        // Создаем объект с информацией о теге и добавляем его в массив тегов
        var tag = {
            name: tagName,
            color: tagColor
        };

        tags.push(tag);
    }

    formData.append('nameProject', nameProject);
    var tagsString = JSON.stringify(tags)
    formData.append('tags', tagsString);

    for (var p of formData) {
        console.log(p);
    }

    fetch('/segmentation/upload/project/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log("Всё супер")
            window.location.href = '/segmentation/projects/';
        } else {
            console.error('Ошибка при сохранении данных в базу данных');
        }
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}


function cancel() {
    window.location.href = '/segmentation/projects/';
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Проверяем, начинается ли текущий cookie с нужного нам имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function showUploadForm() {
    $('.container').find('.form-container, .tags').hide(); // Скрываем все формы
    $('.container').find('.upload-form').show(); // Показываем форму для загрузки изображений
}


function showTagsForm() {
    $('.container').find('.form-container, .upload-form').hide(); // Скрываем все формы
    $('.container').find('.tags').show(); // Показываем форму для загрузки тегов
}


function showProjectForm() {
    $('.container').find('.upload-form, .tags').hide(); // Скрываем все формы
    $('.container').find('.form-container').show(); // Показываем форму для названия проекта
}
