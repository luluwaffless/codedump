from PIL import ImageGrab
import mouse
while True:
    rgb = ImageGrab.grab(bbox=(960, 870, 961, 871)).convert("RGB").getpixel((0, 0))
    if rgb == (255, 255, 255) or rgb == (255, 192, 67):
        mouse.click("left")