from settings import led, bulb
from PIL import ImageGrab, Image
from colorsys import rgb_to_hsv
led.turn_on()
led.set_colour(255, 255, 255)
led.set_brightness(1000)
bulb.turn_on()
bulb.set_colour(255, 255, 255)
bulb.set_brightness(1000) 
try:
    while True:
        (r, g, b) = ImageGrab.grab().resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        (preh, pres, prev) = rgb_to_hsv(r/255, g/255, b/255)
        (h, s, v) = (preh, min(pres*4, 1), min(prev*2, 1))
        led.set_hsv(h, s, v)
        bulb.set_hsv(h, s, v)
except KeyboardInterrupt:
    bulb.turn_off()
    led.turn_off()