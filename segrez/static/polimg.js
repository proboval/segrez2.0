const canvas = document.getElementById('myCanvas');
var abc = 1;
const context = canvas.getContext('2d');
var tempTag = "";
var tempArr = [];
let isDrawing = false;
let k = 0;
let numImg = 1;
const totalObj = n;
let rectForImage = new Array(n)
var colorPolArr = new Array(n);
let flag = 0;

const tagsCont = document.getElementById("tagsSelect");
var colorArr = new Array(3);

//функция запускается только во время открытия окна

// отрисовка точек
canvas.addEventListener('mousedown', function(e) {
    console.log('mousedown');
    isDrawing = true;
    drawPoint(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
});

canvas.addEventListener('mouseup', function() {
    isDrawing = false;
});

/*отрисовка точек*/
function drawPoint(x, y) {
    context.fillRect(x, y, 1, 1); // Рисование точки
    tempArr.push([x, y]);
}

function fillR(points) {
    context.beginPath();
    context.moveTo(points[0][0], points[0][1]);
    for (let i = 1; i < points.length; i++) {
        context.lineTo(points[i][0], points[i][1]);
    }
    context.closePath();
    context.fill();
}

window.addEventListener('keydown', function(event) {
    console.log('press');
    /*вызов отрисовки многоугольника*/
    if (event.key === 'Enter' || event.keyCode === 13) {
        if (tempArr.length > 2){
            console.log('Print Enter');
            saveRectToDB();
            rectForImage[numImg - 1].push(tempArr.slice());
            drawR(rectForImage[numImg - 1][k]);
            fillR(rectForImage[numImg - 1][k]);
            k += 1;
            tempArr = [];
            colorPolArr[numImg - 1].push(tempTag);
            addTableRow(k, tempTag, context.strokeStyle);
        }
    }
    /*следующее изображение*/
    if (event.keyCode === 39) {
        if (numImg < totalObj) {
            numImg += 1;
            drawImageAndPolygons(numImg);
            refreshTable();
            tempArr = [];
            refreshNumberImg();
        }
    }
    /*предыдущее изображение*/
    if (event.keyCode === 37) {
        if (numImg > 1) {
            numImg -= 1;
            drawImageAndPolygons(numImg);
            refreshTable();
            tempArr = [];
            refreshNumberImg();
        }
    }
    console.log(numImg);
});

// Функция для отрисовки многоугольников
function drawPolygons() {
    k = 0;
    for (let i = 0; i < rectForImage[numImg - 1].length; i++) {
        context.strokeStyle = `rgb(${dictTags[colorPolArr[numImg - 1][i]][0]}, ${dictTags[colorPolArr[numImg - 1][i]][1]}, ${dictTags[colorPolArr[numImg - 1][i]][2]})`;
        drawR(rectForImage[numImg - 1][i]);
        k += 1;
    }
     changeOption();
}

// Измененная функция для отрисовки изображения и многоугольников
function drawImageAndPolygons(numImg) {
    $.ajax({
        url: 'get_image_name',
        type: 'GET',
        data: {
            'numImg': numImg
        },
        success: function(data) {
            k = 0;
            drawImage(data['image_url']);
        }
    });

    // Функция для отрисовки только изображения
    function drawImage(imgUrl) {
        let img = new Image();
        img.src = imgUrl;
        img.onload = function() {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(img, 0, 0, img.width, img.height);
            drawPolygons();
        }
    }
}


function refreshNumberImg () {
    var textNumberImg = document.getElementById("imageNumberText");
    textNumberImg.textContent = "Номер изображения: " + numImg;
}


/*отрисовка многоугольника*/
function drawR(matrix) {
    context.beginPath();

    context.moveTo(matrix[0][0], matrix[0][1]);
    for (let i = 1; i < matrix.length; i++) {
        context.lineTo(matrix[i][0], matrix[i][1]);
    }
    context.lineTo(matrix[0][0], matrix[0][1]);
    context.stroke();
}

/*очистка канвы*/
function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
}

function changeOption(){
    let optionName = tagsCont.options[tagsCont.options.selectedIndex].text;
    tempTag = optionName;
    console.log(optionName);
    var color_box = document.getElementById("colorBox");
    color_box.style.backgroundColor = `rgb(${dictTags[optionName][0]}, ${dictTags[optionName][1]}, ${dictTags[optionName][2]})`;
    context.strokeStyle = `rgb(${dictTags[optionName][0]}, ${dictTags[optionName][1]}, ${dictTags[optionName][2]})`;
    context.fillStyle = `rgb(${dictTags[optionName][0]}, ${dictTags[optionName][1]}, ${dictTags[optionName][2]})`;
}

function addTableRow(number, tagName, color) {
    let table = document.getElementById("tableBody");

    let row = table.insertRow(-1);
    row.id = "row_" + number;
    let c1 = row.insertCell(0);
    let c2 = row.insertCell(1);
    let c3 = row.insertCell(2);
    let c4 = row.insertCell(3);

    c1.innerText = number;
    c2.innerText = tagName;
    let box = `<div id='colorBoxTable' class='color-box' style='background-color:${color}'></div>`;
    c3.innerHTML = box;
    // Создаем SVG элемент
    var svgCross = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgCross.setAttribute("class", "red-cross");
    svgCross.setAttribute("width", "16");
    svgCross.setAttribute("height", "16");
    svgCross.setAttribute("viewBox", "0 0 16 16");

    // Создаем линии крестика
    var line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line1.setAttribute("x1", "4"); // Начало первой линии с левого края
    line1.setAttribute("y1", "4"); // Начало первой линии с верхнего края
    line1.setAttribute("x2", "12"); // Конец первой линии вправо
    line1.setAttribute("y2", "12"); // Конец первой линии вниз
    line1.setAttribute("style", "stroke:red;stroke-width:1");

    var line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line2.setAttribute("x1", "12"); // Начало второй линии с правого края
    line2.setAttribute("y1", "4"); // Начало второй линии с верхнего края
    line2.setAttribute("x2", "4"); // Конец второй линии влево
    line2.setAttribute("y2", "12"); // Конец второй линии вниз
    line2.setAttribute("style", "stroke:red;stroke-width:1");

    // Добавляем линии крестика в SVG элемент
    svgCross.appendChild(line1);
    svgCross.appendChild(line2);

    // Добавляем обработчик события для крестика
    svgCross.addEventListener('click', function() {
        delSpace(number);
    });

    // Изменяем стиль курсора при наведении
    svgCross.style.cursor = "pointer";

    // Добавляем SVG элемент в ячейку таблицы
    c4.appendChild(svgCross);
}


function delSpace(number) {
    var row = document.getElementById("row_" + number);
    if (row) {
        delRectDB(number);
        row.parentNode.removeChild(row);
        colorPolArr[numImg - 1].splice(number - 1, 1);
        rectForImage[numImg - 1].splice(number - 1, 1);
        refreshTable();
        drawImageAndPolygons(numImg);
    }
}


function delRectDB(number) {
    let data = {
        "numPolygon": number,
        "numImg": numImg
    }

    fetch('/segmentation/test/del_polygon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            const s = `Полигон номер ${rectForImage[numImg - 1].length + 1} в изображении ${numImg} успешно удалён из базы данных`;
            console.log(s);
        } else {
            console.error('Ошибка при сохранении данных в базу данных');
        }
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}


function refreshTable() {
    let table = document.getElementById("tableBody");
    while(table.rows.length > 0) {
        table.deleteRow(0);
    }

    for (let i = 0; i < colorPolArr[numImg - 1].length; i++) {
        var colorBox = `rgb(${dictTags[colorPolArr[numImg - 1][i]][0]}, ${dictTags[colorPolArr[numImg - 1][i]][1]}, ${dictTags[colorPolArr[numImg - 1][i]][2]})`;
        addTableRow(i + 1, colorPolArr[numImg - 1][i], colorBox)
    }
}


function saveRectToDB() {
    let data = {
        "polygon": tempArr.slice(),
        "numPolygon": rectForImage[numImg - 1].length + 1,
        "numImg": numImg,
        "tag": tempTag
    }

    fetch('/segmentation/test/save_polygon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            const s = `Полигон номер ${rectForImage[numImg - 1].length + 1} в изображении ${numImg} успешно сохранены в базу данных`;
            console.log(s);
        } else {
            console.error('Ошибка при сохранении данных в базу данных');
        }
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}


tagsCont.addEventListener("change", changeOption);