from settings import bulb, led
try:
    while True:
        cmd = input("> ")
        if cmd == "help":
            print('led/bulb/both\n    .turn_on()\n    .turn_off()\n    .set_colour(r, g, b) [0-255]\n    .set_hsv(h, s, v) [0-1]\n    .set_white(brightness, temp) [0-1000]\n    .set_brightness(0-1000)')
        elif cmd == "exit":
            break
        elif cmd.startswith("both."):
            func = cmd.split(".")[1]
            ledExec = exec(f"led.{func}")
            bulbExec = exec(f"bulb.{func}")
            if func == "status()" or func == "state()":
                print(f"LED: {ledExec}, Bulb: {bulbExec}")
        else:
            cmdExec = exec(cmd)
            if cmd.endswith("status()") or cmd.endswith("state()"):
                print(cmdExec)
            
except KeyboardInterrupt:
    pass