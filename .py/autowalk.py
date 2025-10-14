import keyboard
import time
import os
keys = ["w", "s", "d", "a"]
os.system('cls')
for i in range(5):
    print(f"make sure you stay on the roblox window, you have {str(5 - i)} seconds!")
    time.sleep(1)
    os.system('cls')
print("hold Q to stop the program")
while True:
    for key in keys:
        keyboard.press(key)
        time.sleep(0.25)
        keyboard.release(key)
    try:
        if keyboard.is_pressed('q'):
            print("ending")
            break
    except:
        os.system('cls')
        print("hold Q to stop the program")