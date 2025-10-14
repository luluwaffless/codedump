
from os import system
from time import sleep
try:
    from keyboard import is_pressed
    from PIL import ImageGrab
    from pygame import mixer
except ImportError:
    print("please install the required libraries by running the following commands:\npip install keyboard\npip install Pillow\npip install pygame")
    exit()

pc = 0.25 # percentage
x1 = 254 # start of stamina bar
x2 = 478 # end of stamina bar
y = 1016 # height of stamina bar

x = x1+((x2-x1+1)*pc)
bbox = (int(x), int(y), int(x)+1, int(y)+1)
pressed = False
playing = False
mixer.init()
mixer.music.load('alarm.mp3')
try:
    system('title stamina manager')
    system('cls')
    while True:
        if is_pressed('shift'):
            if not pressed:
                pressed = True
            elif not playing and ImageGrab.grab(bbox=bbox).convert('L').getpixel((0, 0)) < 200:
                playing = True
                mixer.music.play(loops=-1)
        else:
            if pressed:
                pressed = False
                if playing:
                    mixer.music.stop()
                    playing = False
        sleep(0.1)
except KeyboardInterrupt:
    if playing:
        mixer.music.stop()
    print("Exiting...")