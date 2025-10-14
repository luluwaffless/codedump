import pyautogui
from PIL import Image
import time
import requests
BOUND_X, BOUND_Y, BOUND_W, BOUND_H = 15, 69, 461, 258
COLORS = {
#    "mythical/shark hunt": (255, 62, 120),
#    "thread": (52, 99, 255),
#    "legendary/streak": (255, 192, 116),
#    "limited": (54, 73, 159),
    "megalodon spawn": (228, 8, 10),
#    "night of the fireflies": (182, 175, 255),
#    "mutation surge": (120, 230, 100)
}
TOLERANCE = 10
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1314066724282302546/jgCnvSmlF6e_O2wN9ysTToj3yX5-F41qR4wMSLjAQnwXJlECRz9MMwQJsj36pBjykyrf"

def is_within_tolerance(pixel_color, target_color):
    return all(abs(pixel_color[i] - target_color[i]) <= TOLERANCE for i in range(3))
def find_colors_in_region():
    screenshot = pyautogui.screenshot(region=(BOUND_X, BOUND_Y, BOUND_W, BOUND_H))
    screenshot = screenshot.convert("RGB")
    detected_colors = set()
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            pixel_color = screenshot.getpixel((x, y))
            for color_name, target_color in COLORS.items():
                if is_within_tolerance(pixel_color, target_color):
                    detected_colors.add(color_name)
    return detected_colors, screenshot
def send_to_discord(screenshot, message):
    screenshot.save("temp_screenshot.png")
    payload = {"content": message}
    files = {"file": open("temp_screenshot.png", "rb")}
    requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
    files["file"].close()
while True:
    detected_colors, screenshot = find_colors_in_region()
    if detected_colors:
        message = f"@everyone {", ".join(detected_colors)}"
        print(message)
        send_to_discord(screenshot, message)
    time.sleep(15)