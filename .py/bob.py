from pyautogui import moveTo
from keyboard import is_pressed
from time import sleep
sleep(2)
while True:
    if is_pressed('q'):
        break
    moveTo(480, 540)
    sleep(1)
    moveTo(1440, 540)
    sleep(1)