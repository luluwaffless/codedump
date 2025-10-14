from keyboard import press_and_release
from pyautogui import click
from PIL import ImageGrab
from time import sleep, time, strftime
analytics = {
    "startTime": time(),
    "startStr": strftime("%Y-%m-%d %H:%M:%S"),
    "stews": 0,
    "times": []
}

print("99NITF macro by luluwaffless\nswitch to your roblox window in the next 3 seconds")
sleep(3)
print("starting... press Ctrl+C to stop")
last_time = 0

try:
    while True:
        pixel = ImageGrab.grab(bbox=(47, 504, 48, 505)).convert("RGB").getpixel((0, 0))

        if pixel != (255, 123, 57): # if character is hungry
            now = time() 
            if now - last_time >= 60: # only count new hunger if 60s have passed since last one
                analytics["stews"] += 1
                analytics["times"].append(now)
                if len(analytics["times"]) > 1:
                    intervals = [analytics["times"][i + 1] - analytics["times"][i] for i in range(len(analytics["times"]) - 1)]
                    avg = sum(intervals) / len(intervals)
                else:
                    avg = 0
                avg_m = int(avg // 60)
                avg_s = int(avg % 60)
                print(f"[{strftime('%H:%M:%S')}] eating stew #{analytics['stews']}, " f"avg interval: {avg_m}m {avg_s}s")
                last_time = now
                press_and_release('9') # equip stew
                sleep(0.2)

        click() # anti-afk / activate stew
        sleep(30)

except KeyboardInterrupt:
    print("stopping...")
    end_time = time()
    session_length = end_time - analytics["startTime"]
    hrs = int(session_length // 3600)
    mins = int((session_length % 3600) // 60)
    secs = int(session_length % 60)
    if len(analytics["times"]) > 1:
        intervals = [analytics["times"][i + 1] - analytics["times"][i] for i in range(len(analytics["times"]) - 1)]
        avg = sum(intervals) / len(intervals)
        avg_m = int(avg // 60)
        avg_s = int(avg % 60)
    else:
        avg_m = avg_s = 0

    print(f"\n--- session summary ---\nstart time: {analytics['startStr']}\ntotal stews eaten: {analytics['stews']}\naverage hunger interval: {avg_m}m {avg_s}s\ntotal session length: {hrs}h {mins}m {secs}s")
    exit(0)