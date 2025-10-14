from keyboard import press_and_release, is_pressed
from time import sleep
while True:
    if is_pressed('q'):
        break
    press_and_release('e')
    press_and_release('r')
    press_and_release('enter')
    sleep(0.1)