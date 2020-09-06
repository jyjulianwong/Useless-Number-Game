var memeCanvas = $("#memeCanvas")[0];
var memeCanvasContext = memeCanvas.getContext("2d");

const imgNormalSize = 240;
const imgExtremeSize = 360;

var babyImYoursNormal = $("#babyImYoursNormal")[0];
babyImYoursNormal.loop = true;
babyImYoursNormal.volume = 0.5;

var babyImYoursExtreme = $("#babyImYoursExtreme")[0];
babyImYoursExtreme.loop = true;
babyImYoursExtreme.volume = 0.1;

var imgNormal = new Image();
imgNormal.src = "/static/content/img_um1_normal.png";
imgNormal.width = imgNormalSize;
imgNormal.height = imgNormalSize;

var imgExtreme = new Image();
imgExtreme.src = "/static/content/img_um1_extreme.png";
imgExtreme.width = imgExtremeSize;
imgExtreme.height = imgExtremeSize;

var imageAngle = 0;
var frameInterval = 100;
var isMemeActivated = false;
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

function animateMemeNormal() {
    animator = setInterval(function () {drawNextFrame(imgNormal);}, frameInterval);
    return animator;
}

function animateMemeExtreme() {
    if (isMemeActivated) {
        babyImYoursNormal.pause();
        clearInterval(animator);

        babyImYoursExtreme.play();
        $("#btnCrackhead")[0].disabled = true;
        $("#btnCrackhead")[0].innerHTML = "SIKE";
        animator = setInterval(function () {drawNextFrame(imgExtreme);}, frameInterval);
        return animator;
    }

    isMemeActivated = true;
    babyImYoursNormal.play();
    $("#btnCrackhead")[0].className = "buttonNav buttonRed";
    $("#btnCrackhead")[0].innerHTML = "CRACKHEAD";
    animateMemeNormal();
}

$(document).ready(function () {
    babyImYoursNormal.load();
    babyImYoursExtreme.load();
    $("#btnCrackhead")[0].disabled = false;
    $("#btnCrackhead")[0].innerHTML = "Wtf? 🔊";
    drawNextFrame(imgNormal);
});
