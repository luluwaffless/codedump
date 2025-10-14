from keyboard import press, release, press_and_release
from time import sleep
for i in range(5):
    print(f"switch to the roblox window, starting in {5-(i)}")
    sleep(1)
print("this should take 2 minutes and 28 seconds")
for key in "asdwasdwwasdwwasdsdwasdwwassddwsawdsawwdssawdsawwdsaasawddssawdsawddwassdwasdwaasdwaasdddwaasdwaasddwwassddwasdwsawdsawwdssawdsawwdssawdsadwaasdwds":
    press(key)
    sleep(0.333)
    release(key)
    sleep(0.25)
    press_and_release("e")
    sleep(0.25)