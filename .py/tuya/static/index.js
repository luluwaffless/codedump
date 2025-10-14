const deviceSelect = document.getElementById("device");
const deleteOption = document.getElementById("delete");
const controlsDiv = document.getElementById("controls");
const switchBool = document.getElementById("switch");
const modeDiv = document.getElementById("modeDiv");
const modeSelect = document.getElementById("mode");
const whiteDiv = document.getElementById("white");
const whiteAdvancedBool = document.getElementById("whiteAdvanced");
const colourDiv = document.getElementById("colour");
const brightnessRange = document.getElementById("brightness");
const temperatureRange = document.getElementById("temperature");
const colorInput = document.getElementById("color");
const colourRegularDiv = document.getElementById("colourRegular");
const colourAdvancedDiv = document.getElementById("colourAdvanced");
const colourAdvancedBool = document.getElementById("colourAdvancedBool");
const hueNumber = document.getElementById("hue");
const saturationNumber = document.getElementById("saturation");
const valueNumber = document.getElementById("value");
const bulb = new WebSocket("wss://192.168.0.61/ws/bulb");
const led = new WebSocket("wss://192.168.0.61/ws/led");
const hexToHsv = hex => [parseInt(hex.slice(0, 4), 16), parseInt(hex.slice(4, 8), 16) / 1000, parseInt(hex.slice(8, 12), 16) / 1000];
const hsvToHex = (h, s, v) => (Math.round(h).toString(16).padStart(4, '0') + Math.round(s * 1000).toString(16).padStart(4, '0') + Math.round(v * 1000).toString(16).padStart(4, '0'))
const rgbToHsv = hex => {
    const rNorm = parseInt(hex.slice(1, 3), 16) / 255;
    const gNorm = parseInt(hex.slice(3, 5), 16) / 255;
    const bNorm = parseInt(hex.slice(5, 7), 16) / 255;
    const max = Math.max(rNorm, gNorm, bNorm);
    const delta = max - Math.min(rNorm, gNorm, bNorm);
    let h = 0;
    if (delta !== 0) {
        if (max === rNorm) {
            h = ((gNorm - bNorm) / delta) % 6;
        } else if (max === gNorm) {
            h = (bNorm - rNorm) / delta + 2;
        } else {
            h = (rNorm - gNorm) / delta + 4;
        };
        h *= 60;
        if (h < 0) h += 360;
    };
    return hsvToHex(h, max === 0 ? 0 : delta / max, max);
};
const hsvToRgb = hex => {
    const [h, s, v] = hexToHsv(hex);
    const c = v * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = v - c;
    let r = 0, g = 0, b = 0;
    if (h < 60) [r, g, b] = [c, x, 0];
    else if (h < 120) [r, g, b] = [x, c, 0];
    else if (h < 180) [r, g, b] = [0, c, x];
    else if (h < 240) [r, g, b] = [0, x, c];
    else if (h < 300) [r, g, b] = [x, 0, c];
    else [r, g, b] = [c, 0, x];
    const toHex = val => Math.round((val + m) * 255).toString(16).padStart(2, '0');
    return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
};
const loadDevice = (state) => {
    const [h, s, v] = hexToHsv(state.colour);
    switchBool.checked = state.switch;
    modeSelect.value = state.mode;
    modeDiv.style.display = state.switch ? "block" : "none";
    whiteDiv.style.display = state.mode === "white" ? "block" : "none";
    colourDiv.style.display = state.mode === "colour" ? "block" : "none";
    brightnessRange.value = state.brightness;
    temperatureRange.value = state.temperature;
    colorInput.value = hsvToRgb(state.colour);
    hueNumber.value = h;
    saturationNumber.value = s * 1000;
    valueNumber.value = v * 1000;
    controlsDiv.style.display = "block";
};
bulb.onopen = () => console.log("Bulb WebSocket connection established");
led.onopen = () => console.log("LED WebSocket connection established");
bulb.onmessage = (response) => {
    if (deviceSelect.value === "bulb") loadDevice(JSON.parse(response.data));
};
led.onmessage = (response) => {
    if (deviceSelect.value === "led") loadDevice(JSON.parse(response.data));
};

let deletedOption = false;
deviceSelect.addEventListener("change", () => {
    const device = deviceSelect.value;
    if (!deletedOption) {
        deleteOption.remove();
        deletedOption = true;
    };
    controlsDiv.style.display = "none";
    if (device === "bulb") bulb.send("state");
    else if (device === "led") led.send("state");
});
switchBool.addEventListener("change", () => {
    modeDiv.style.display = switchBool.checked ? "block" : "none"
    if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ switch: switchBool.checked }));
    else if (deviceSelect.value === "led") led.send(JSON.stringify({ switch: switchBool.checked }));
});
modeSelect.addEventListener("change", () => {
    if (modeSelect.value === "white") {
        whiteDiv.style.display = "block";
        colourDiv.style.display = "none";
        if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ mode: "white", brightness: brightnessRange.value, temperature: temperatureRange.value }));
        else if (deviceSelect.value === "led") led.send(JSON.stringify({ mode: "white", brightness: brightnessRange.value, temperature: temperatureRange.value }));
    } else if (modeSelect.value === "colour") {
        whiteDiv.style.display = "none";
        colourDiv.style.display = "block";
        if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ mode: "colour", colour: rgbToHsv(colorInput.value) }));
        else if (deviceSelect.value === "led") led.send(JSON.stringify({ mode: "colour", colour: rgbToHsv(colorInput.value) }));
    };
});
brightnessRange.addEventListener("input", () => {
    if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ brightness: brightnessRange.value }));
    else if (deviceSelect.value === "led") led.send(JSON.stringify({ brightness: brightnessRange.value }));
});
temperatureRange.addEventListener("input", () => {
    if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ temperature: temperatureRange.value }));
    else if (deviceSelect.value === "led") led.send(JSON.stringify({ temperature: temperatureRange.value }));
});
whiteAdvancedBool.addEventListener("change", () => {
    brightnessRange.setAttribute("type", whiteAdvancedBool.checked ? "number" : "range")
    temperatureRange.setAttribute("type", whiteAdvancedBool.checked ? "number" : "range")
})
colorInput.addEventListener("input", () => {
    const hex = rgbToHsv(colorInput.value);
    const [h, s, v] = hexToHsv(hex);
    hueNumber.value = h;
    saturationNumber.value = s * 1000;
    valueNumber.value = v * 1000;
    if (deviceSelect.value === "bulb") bulb.send(JSON.stringify({ mode: "colour", colour: hex }));
    else if (deviceSelect.value === "led") led.send(JSON.stringify({ mode: "colour", colour: hex }));
});
colourAdvancedBool.addEventListener("change", () => {
    colourRegularDiv.style.display = colourAdvancedBool.checked ? "none" : "block";
    colourAdvancedDiv.style.display = colourAdvancedBool.checked ? "block" : "none";
});
const hsvCallback = () => {
    const hex = hsvToHex(hueNumber.value, saturationNumber.value / 1000, valueNumber.value / 1000);
    colorInput.value = hsvToRgb(hex);
    if (deviceSelect.value === "bulb") {
        bulb.send(JSON.stringify({ mode: "colour", colour: hex }));
    } else if (deviceSelect.value === "led") {
        led.send(JSON.stringify({ mode: "colour", colour: hex }));
    };
};
hueNumber.addEventListener("input", hsvCallback);
saturationNumber.addEventListener("input", hsvCallback);
valueNumber.addEventListener("input", hsvCallback);