var isPlaying = false;
var number1 = 0;
var number2 = 0;
var symbolValue = 0;
var symbol = "";
var answer = 0;
var answerA = 0;
var answerB = 0;
var answerC = 0;
var answerD = 0;
var answeredTotal = 0;
var answeredCorrect = 0;
var scorePercent = 0;
var timerValue = 0;

const timerInit = 10;

const uselessStatements1 = [
    "This is stupid…",
    "Do something more productive…",
    "Okay, I'm bored as well…",
    "Why are you still here?!"
];

const uselessStatements2 = [
    "Are you really that bored?",
    "Get a life.",
    "Bored coding this stupid website.",
    "There's more to life than this."
];

function roundToDecimal(number, precision) {
    var numberStr = number.toFixed(precision);
    numberRnd = parseFloat(numberStr);
    return numberRnd;
}

function createAnswerOffset() {
    return Math.floor((Math.random() * 25)) - Math.floor((Math.random() * 25));
}

function init() {
    isPlaying = false;
    symbolValue = 0;
    number1 = 0;
    number2 = 0;
    symbol = "";
    answer = 0;
    answerA = 0;
    answerB = 0;
    answerC = 0;
    answerD = 0;
    answeredTotal = 0;
    answeredCorrect = 0;
    scorePercent = 0;
    timerValue = 0;

    document.getElementById("divStart").style.display = 'block';
    document.getElementById("question").innerHTML = "";
    document.getElementById("score").innerHTML = "";
    document.getElementById("timer").style.display = 'none';
    document.getElementById("timer").innerHTML = "";
    document.getElementById("btnAnswerA").innerHTML = "A";
    document.getElementById("btnAnswerB").innerHTML = "B";
    document.getElementById("btnAnswerC").innerHTML = "C";
    document.getElementById("btnAnswerD").innerHTML = "D";
}

function start() {
    isPlaying = true;
    document.getElementById("divStart").style.display = 'none';
    document.getElementById("timer").style.display = 'block';
    document.getElementById("question").style.color = "#ffffff";
    createNewQuestion(true);

    timerValue = timerInit + 1;
    timerUpdate();
    timer = setInterval(timerUpdate, 1000);
}

function createNewQuestion(isFirstQuestion) {
    number1 = Math.floor((Math.random() * 50) + 5);
    number2 = Math.floor((Math.random() * 50) + 5);
    symbolValue = Math.floor((Math.random() * 4)) + 1;
    switch (symbolValue) {
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
        default:
            answer = number1 / number2;
            symbol = " / ";
            break;
    }

    let randomOption = Math.floor((Math.random() * 4)) + 1;
    switch (randomOption) {
        case 1:
            answerA = answer;
            answerB = answer + createAnswerOffset();
            answerC = answer + createAnswerOffset();
            answerD = answer + createAnswerOffset();
            break;
        case 2:
            answerA = answer + createAnswerOffset();
            answerB = answer;
            answerC = answer + createAnswerOffset();
            answerD = answer + createAnswerOffset();
            break;
        case 3:
            answerA = answer + createAnswerOffset();
            answerB = answer + createAnswerOffset();
            answerC = answer;
            answerD = answer + createAnswerOffset();
            break;
        default:
            answerA = answer + createAnswerOffset();
            answerB = answer + createAnswerOffset();
            answerC = answer + createAnswerOffset();
            answerD = answer;
            break;
    }

    checkRepeatedAnswers();

    if (answeredTotal == 0) {
        scorePercent = 0;
    } else {
        scorePercent = Math.round((answeredCorrect / answeredTotal) * 100);
    }

    answer = roundToDecimal(answer, 2);
    answerA = roundToDecimal(answerA, 2);
    answerB = roundToDecimal(answerB, 2);
    answerC = roundToDecimal(answerC, 2);
    answerD = roundToDecimal(answerD, 2);
    document.getElementById("question").innerHTML = String(number1) + symbol + String(number2);
    document.getElementById("score").innerHTML = "Your score is " + String(answeredCorrect) + " / " + String(answeredTotal) + ", or " + String(scorePercent) + "%.";
    document.getElementById("btnAnswerA").innerHTML = String(answerA);
    document.getElementById("btnAnswerB").innerHTML = String(answerB);
    document.getElementById("btnAnswerC").innerHTML = String(answerC);
    document.getElementById("btnAnswerD").innerHTML = String(answerD);

    if (!isFirstQuestion) {
        checkIsGameOver();
    }
}

function timerUpdate() {
    if (timerValue == 0) {
        answeredTotal += 1;
        timerValue = timerInit;
        createNewQuestion(false);
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

function checkRepeatedAnswers() {
    if (answerA == answerB || answerA == answerC || answerA == answerD || answerB == answerC || answerB == answerD || answerC == answerD) {
        createNewQuestion(false);
    }
}

function checkIsGameOver() {
    if (scorePercent < 50) {
        clearInterval(timer);
        init();
        document.getElementById("question").style.color = "#ff9988";
        document.getElementById("question").innerHTML = "You've failed the test. Again?";
        document.getElementById("score").innerHTML = "You know you need 50% to pass, right?";
    }
}

function checkAnswer(option) {
    let selectedAnswer;
    switch (option) {
        case "a":
            selectedAnswer = answerA;
            break;
        case "b":
            selectedAnswer = answerB;
            break;
        case "c":
            selectedAnswer = answerC;
            break;
        case "d":
            selectedAnswer = answerD;
            break;
    }

    if (isPlaying) {
        answeredTotal += 1;
        timerValue = timerInit + 1;
        if (selectedAnswer == String(answer)) {
            answeredCorrect += 1;
        }
        createNewQuestion(false);
    } else {
        let randomIndex = Math.floor(Math.random() * uselessStatements1.length);
        document.getElementById("score").innerHTML = uselessStatements1[randomIndex];
        document.getElementById("question").innerHTML = uselessStatements2[randomIndex];
    }
}
