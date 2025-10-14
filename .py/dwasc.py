from PIL import ImageGrab
from pymsgbox import alert
import keyboard
alert(text="made by luluwaffless", title="dandy's world auto skill check", button="OK")

while True:
    good = []
    cursor = []
    minPos = 0
    cursorPos = 0
    rgb = ImageGrab.grab(bbox=(672, 842, 1247, 843)).convert("RGB")
    width, height = rgb.size
    
    for x in range(width):
        goodDifference = [abs(a - b) for a, b in zip((255, 255, 255), rgb.getpixel((x, 0)))]
        goodAverage = sum(goodDifference) / len(goodDifference)
        
        cursorDifference = [abs(a - b) for a, b in zip((255, 87, 90), rgb.getpixel((x, 0)))]
        cursorAverage = sum(cursorDifference) / len(cursorDifference)
        
        if goodAverage <= 10:
            good.append(x)
        elif cursorAverage <= 10:
            cursor.append(x)
    
    if len(good) >= 2 and len(cursor) >= 2:
        cursorPos = min(cursor)
        minPos = min(good)
        if cursorPos >= minPos:
            keyboard.press_and_release('space')
