var memeCanvas = document.getElementById("memeCanvas");
var memeCanvasContext = memeCanvas.getContext("2d");

const sizeNormal = 240;
const sizeExtreme = 360;

var imgNormal = new Image();
imgNormal.src = "/static/content/img_um1_normal.png";
imgNormal.width = sizeNormal;
imgNormal.height = sizeNormal;

var imgExtreme = new Image();
imgExtreme.src = "/static/content/img_um1_extreme.png";
imgExtreme.width = sizeExtreme;
imgExtreme.height = sizeExtreme;

var imageAngle = 0;
var frameInterval = 100;
var isMemeActivated = false;
var animator;

var babyImYoursNormal = document.getElementById("babyImYoursNormal");
babyImYoursNormal.loop = true;
babyImYoursNormal.volume = 0.5;
var babyImYoursExtreme = document.getElementById("babyImYoursExtreme");
babyImYoursExtreme.loop = true;
babyImYoursExtreme.volume = 0.1;

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
    document.getElementById("btnCrackhead").style.visibility = "hidden";

    babyImYoursExtreme.play();
    animator = setInterval(function () {drawNextFrame(imgExtreme);}, frameInterval);
    return animator;
  }

  babyImYoursNormal.play();
  document.getElementById("btnCrackhead").innerHTML = "Crackhead";
  animateMemeNormal();
  isMemeActivated = true;
}

drawNextFrame(imgNormal);
