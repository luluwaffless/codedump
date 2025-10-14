# lulu was here
from time import sleep
import pyautogui
import keyboard
ALTS = [ # alt windows (to keep alive)
    (400, 315),
    (400, 764),
    (1360, 330)
]
MAIN = (1530, 870) # main window, exactly where the quest button is located
DELAY = 0.25 # delay between actions

print("starting in 5 seconds, switch to your roblox windows")
sleep(5) # time to switch to show your windows
print("starting macro")
while True:
    if keyboard.is_pressed('q'): # hold q to quit
        print("bye bye!")
        break
    
    # keep alts alive
    for alt in ALTS:
        pyautogui.moveTo(alt)
        for _ in range(5):
            pyautogui.click(alt)
            sleep(DELAY)
        
    # restart quest
    pyautogui.moveTo(MAIN)
    pyautogui.click(MAIN)
    keyboard.press_and_release("e")
    sleep(0.5)
    for _ in range(5):
        keyboard.press_and_release("e")
        pyautogui.click(MAIN)
        sleep(DELAY)