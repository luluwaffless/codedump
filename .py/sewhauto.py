import keyboard
import random
import time
keys = ["w", "a", "s", "d"]
opposite = {
    "w": "s",
    "a": "d",
    "s": "w",
    "d": "a"
}
while True:
    for key in keys:
        t = random.randint(1, 500) / 1000
        keyboard.press(key)
        time.sleep(t)
        keyboard.release(key)
        keyboard.press(opposite[key])
        time.sleep(t)
        keyboard.release(opposite[key])