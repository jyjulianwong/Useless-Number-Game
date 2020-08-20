var timerInit = 10;

var play = 0;
var opMode = 0;
var number1 = 0;
var number2 = 0;
var symbol = "";
var answer = 0;
var answerA = 0;
var answerB = 0;
var answerC = 0;
var answerD = 0;
var answerLoc = 0;
var answeredTotal = 0;
var answeredCorrect = 0;
var scorePercent = 0;
var timerValue = 0;

function precisionRound(number, precision) {
    var numberStr = number.toFixed(precision);
    numberRnd = parseFloat(numberStr);
    return numberRnd;
}

function init() {
    play = 0;
    opMode = 0;
    number1 = 0;
    number2 = 0;
    symbol = "";
    answer = 0;
    answerA = 0;
    answerB = 0;
    answerC = 0;
    answerD = 0;
    answerLoc = 0;
    answeredTotal = 0;
    answeredCorrect = 0;
    scorePercent = 0;
    timerValue = 0;

    document.getElementById('divStart').style.display = 'block';
    document.getElementById('divMainBack').style.marginTop = '25px';
    document.getElementById("question").innerHTML = "";
    document.getElementById("score").innerHTML = "";
    document.getElementById("timer").innerHTML = "";
    document.getElementById("btnAnswerA").innerHTML = "A";
    document.getElementById("btnAnswerB").innerHTML = "B";
    document.getElementById("btnAnswerC").innerHTML = "C";
    document.getElementById("btnAnswerD").innerHTML = "D";
}

function start() {
    play = 1;
    quesGenerate(1);
    document.getElementById('divStart').style.display = 'none';
    document.getElementById('divMainBack').style.marginTop = '50px';
    document.getElementById("question").style.color = "#ffffff";

    timerValue = timerInit + 1;
    timerUpdate();
    timerRefer = setInterval(timerUpdate, 1000);
}

function quesGenerate(start) {
    number1 = Math.floor((Math.random() * 50) + 5);
    number2 = Math.floor((Math.random() * 50) + 5);
    opMode = Math.floor((Math.random() * 4)) + 1;
    switch (opMode) {
        case 1:
            answer = number1 + number2;
            symbol = " + ";
            break;
        case 2:
            answer = number1 - number2;
            symbol = " - ";
            break;
        case 3:
            answer = number1 * number2;
            symbol = " * ";
            break;
        case 4:
            answer = number1 / number2;
            symbol = " / ";
            break;
        default:
            answer = number1 + number2;
            symbol = " + ";
    }

    answerLoc = Math.floor((Math.random() * 4)) + 1;
    switch (answerLoc) {
        case 1:
            answerA = answer;
            answerB = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerC = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerD = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            break;
        case 2:
            answerA = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerB = answer;
            answerC = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerD = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            break;
        case 3:
            answerA = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerB = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerC = answer;
            answerD = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            break;
        case 4:
            answerA = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerB = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerC = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerD = answer;
            break;
        default:
            answerA = answer;
            answerB = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerC = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
            answerD = answer + Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
    }
    answerCheck();

    if (answeredTotal == 0) {
        scorePercent = 0;
    } else {
        scorePercent = Math.round((answeredCorrect / answeredTotal) * 100);
    }

    answer = precisionRound(answer, 2);
    answerA = precisionRound(answerA, 2);
    answerB = precisionRound(answerB, 2);
    answerC = precisionRound(answerC, 2);
    answerD = precisionRound(answerD, 2);
    document.getElementById("question").innerHTML = String(number1) + symbol + String(number2);
    document.getElementById("score").innerHTML = "Your score is " + String(answeredCorrect) + " / " + String(answeredTotal) + ", or " + String(scorePercent) + "%.";
    document.getElementById("btnAnswerA").innerHTML = String(answerA);
    document.getElementById("btnAnswerB").innerHTML = String(answerB);
    document.getElementById("btnAnswerC").innerHTML = String(answerC);
    document.getElementById("btnAnswerD").innerHTML = String(answerD);

    if (start == 0) {
        scoreCheck();
    }
}

function timerUpdate() {
    if (timerValue == 0) {
        answeredTotal += 1;
        timerValue = timerInit;
        quesGenerate(0);
        document.getElementById("timer").innerHTML = "You've got " + String(timerInit) + " seconds left.";
    } else {
        timerValue -= 1;
        if (timerValue == 1) {
            document.getElementById("timer").innerHTML = "You've got " + String(timerValue) + " second left.";
        } else {
            document.getElementById("timer").innerHTML = "You've got " + String(timerValue) + " seconds left.";
        }
    }
}

function answerCheck() {
    if (answerA == answerB || answerA == answerC || answerA == answerD || answerB == answerC || answerB == answerD || answerC == answerD) {
        quesGenerate(0);
    }
}

function scoreCheck() {
    if (scorePercent < 50) {
        clearInterval(timerRefer);
        init();
        document.getElementById("question").style.color = "#ff9988";
        document.getElementById("question").innerHTML = "You've failed the test. Again?";
        document.getElementById("score").innerHTML = "You know you need 50% to pass, right?";
    }
}

function answerAClick() {
    if (play == 1) {
        answeredTotal += 1;
        timerValue = timerInit + 1;
        if (answerA == String(answer)) {
            answeredCorrect += 1;
            quesGenerate(0);
        } else {
            quesGenerate(0);
        }
    } else {
        document.getElementById("score").innerHTML = "This is stupid…";
        document.getElementById("question").innerHTML = "Are you really that bored?";
    }
}

function answerBClick() {
    if (play == 1) {
        answeredTotal += 1;
        timerValue = timerInit + 1;
        if (answerB == String(answer)) {
            answeredCorrect += 1;
            quesGenerate(0);
        } else {
            quesGenerate(0);
        }
    } else {
        document.getElementById("score").innerHTML = "Do something more productive…";
        document.getElementById("question").innerHTML = "Get a life, mate.";
    }
}

function answerCClick() {
    if (play == 1) {
        answeredTotal += 1;
        timerValue = timerInit + 1;
        if (answerC == String(answer)) {
            answeredCorrect += 1;
            quesGenerate(0);
        } else {
            quesGenerate(0);
        }
    } else {
        document.getElementById("score").innerHTML = "Okay, I'm bored as well…";
        document.getElementById("question").innerHTML = "Bored coding this stupid website.";
    }
}

function answerDClick() {
    if (play == 1) {
        answeredTotal += 1;
        timerValue = timerInit + 1;
        if (answerD == String(answer)) {
            answeredCorrect += 1;
            quesGenerate(0);
        } else {
            quesGenerate(0);
        }
    } else {
        document.getElementById("score").innerHTML = "Why are you still here?!";
        document.getElementById("question").innerHTML = "There's more to life than this.";
    }
}