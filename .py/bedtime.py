from winmsgbox import MessageBox, Buttons, Icon, Modal, Flags, Response
from datetime import datetime
from threading import Thread
from time import sleep
from os import system
activeDays = [6, 0, 1, 2, 3]
warnings = 0
def warn():
    global warnings
    response = MessageBox(title="sleep reminder", text="it's almost bedtime... shutdown?", buttons=Buttons.YesNo, icon=Icon.Information, modal=Modal.SystemModal, flags=Flags.SetForeground)
    if response == Response.Yes:
        system('shutdown /s /t 60 /c "good night!"')
    else:
        MessageBox(title="sleep reminder", text=f"{"alright" if warnings < 4 else "this was your last warning"}, you have 30 more minutes", buttons=Buttons.Ok, icon=Icon.Warning, modal=Modal.SystemModal, flags=Flags.SetForeground)
while True:
    now = datetime.now()
    if now.weekday() in activeDays:
        if now.hour >= 22 or (now.hour < 5 and now.weekday() != 6):
            warnings = 5
            system('shutdown /s /t 60 /c "good night!"')
            sleep(90)
        elif now.hour >= 20:
            warnings += 1
            if warnings < 5:
                Thread(target=warn).start()
                sleep(1800)
            else:
                system('shutdown /s /t 60 /c "good night!"')
                sleep(90)
        else:
            warnings = 0
            sleep(60)
    else:
        sleep(3600)