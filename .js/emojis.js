const alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
const numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
const alternatives = {
    'A': ['🅰️'],
    'B': ['🅱️'],
    'O': ['🅾️', '⭕'],
    'P': ['🅿️'],
    'AB': ['🆎'],
    'CL': ['🆑'],
    'COOL': ['🆒'],
    'FREE': ['🆓'],
    'ID': ['🆔'],
    'NEW': ['🆕'],
    'NG': ['🆖'],
    'OK': ['🆗'],
    'SOS': ['🆘'],
    'UP': ['🆙'],
    'VS': ['🆚'],
    'X': ['❌']
};

function letterToEmoji(letter) {
    var upperLetter = letter.toUpperCase();
    if (upperLetter >= 'A' && upperLetter <= 'Z') {
        var offset = upperLetter.charCodeAt(0) - 'A'.charCodeAt(0) + 127462;
        return String.fromCodePoint(offset);
    } else {
        return '';
    };
};
function numberToEmoji(numberStr) {
    var digitEmoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'];
    var emojiRepresentation = '';
    for (var i = 0; i < numberStr.length; i++) {
        var digit = parseInt(numberStr.charAt(i));
        if (!isNaN(digit)) {
            emojiRepresentation += digitEmoji[digit];
        };
    };
    return emojiRepresentation;
};
function getAlternative(char, returnArr) {
    if (alternatives[char]) {
        for (const alt of alternatives[char]) {
            if (!returnArr.includes(alt)) {
                return alt;
            };
        };
    };
    return null;
};
function reactString(str) {
    var returnArr = [];
    for (let i = 0; i < str.length; i++) {
        const char = str.charAt(i);
        if (alphabet.includes(char.toLowerCase())) {
            const emoji = letterToEmoji(char);
            if (emoji && !returnArr.includes(emoji)) {
                returnArr.push(emoji);
            } else {
                const alternative = getAlternative(char.toUpperCase(), returnArr);
                if (alternative && !returnArr.includes(alternative)) {
                    returnArr.push(alternative);
                } else {
                    console.log("no alternative :(");
                };
            };
        } else if (numbers.includes(char)) {
            const emoji = numberToEmoji(char);
            if (emoji && !returnArr.includes(emoji)) {
                returnArr.push(emoji);
            } else {
                const alternative = getAlternative(char.toUpperCase(), returnArr);
                if (alternative && !returnArr.includes(alternative)) {
                    returnArr.push(alternative);
                } else {
                    console.log("no alternative :(");
                };
            };
        };
    };
    return returnArr;
};