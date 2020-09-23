var memeCanvas = $("#memeCanvas")[0];
var memeCanvasContext = memeCanvas.getContext("2d");

const imgSize = 360;

var uwu = $("#uwu")[0];

var img = new Image();
img.src = "/static/content/img_um2_uwu.png";
img.width = imgSize;
img.height = imgSize;

var imageAngle = 0;
var frameInterval = 100;
var animator;

function drawNextFrame(image) {
    memeCanvasContext.save();
    memeCanvasContext.clearRect(0, 0, memeCanvas.width, memeCanvas.height);
    memeCanvasContext.translate(memeCanvas.width / 2, memeCanvas.height / 2);
    memeCanvasContext.rotate(Math.PI / 180 * (imageAngle += 5));
    memeCanvasContext.drawImage(
        image,
        Math.floor(-image.width / 2),
        Math.floor(-image.height / 2),
        image.width,
        image.height
    );
    memeCanvasContext.restore();
}

function animateMeme() {
    uwu.play();
    $("#btnUwu")[0].style.visibility = "hidden";
    $(".bg")[0].style.backgroundColor = "#ffc0cb";
    animator = setInterval(function () {drawNextFrame(img);}, frameInterval);
    return animator;
}

$(document).ready(function () {
    uwu.load();
    $("#btnUwu")[0].disabled = false;
    $("#btnUwu")[0].innerHTML = "Play… 🔊";
});
