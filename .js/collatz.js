const conjecture = (n) => {
    const l = [];
    var c = n;
    while (c !== 1) {
        if (c % 2 === 0) {
            c = c / 2;
        } else {
            c = c * 3;
            c = c + 1;
        };
        l.push(c);
    };
    return l;
};

let highestl = 949;
let ifromhighestl = 63728127;
for (let i = ifromhighestl; i > 0; i++) {
    const l = conjecture(i);
    if (l.length > highestl) {
        highestl = l.length;
        ifromhighestl = i;
        console.log(`New highest length: ${highestl} for number ${ifromhighestl}`);
    };
};