from sounddevice import query_devices, play, wait
from soundfile import read
from numpy import stack
from gtts import gTTS
import keyboard as kb
from os import remove
lang='pt-br'
devices = []
device = None
for i, d in enumerate(query_devices()):
    if d['max_output_channels'] > 0:
        if d['name'] == "Output (VB-Audio Point)":
            print(f"VB-Audio Point device found at index {i}.")
            device = i
        else:
            devices.append(f"{i}: {d['name']} - {d['max_output_channels']} channels")
if not device:
    print(f"VB-Audio Point not found. Available devices:\n{'\n'.join(devices)}")
    device = int(input("Select the device number for your audio cable: "))
    devices.clear()
listening = False
buffer = []
speaking = False
def playFile(filename):
    data, samplerate = read(filename)
    if data.ndim == 1:
        data = stack([data, data], axis=1)
    play(data, samplerate=samplerate, device=device)
    wait()
    return
def speak(text):
    global speaking, device, lang
    if not speaking:
        try:
            speaking = True
            print(text)
            gTTS(text=text, lang=lang, slow=False).save('temp.wav')
            playFile('temp.wav')
            remove('temp.wav')
            speaking = False
        except:
            speaking = False
def on_key(event):
    global listening, buffer, speaking
    if not speaking and event.event_type == 'down':
        key = event.name
        if not listening:
            if key == ';':
                listening = True
                #playFile('writing.wav')
                buffer.clear()
        else:
            if key == 'enter':
                listening = False
                text = ''.join(buffer)
                buffer.clear()
                speak(text)
            elif key == 'space':
                buffer.append(' ')
            elif key == 'backspace' and buffer:
                buffer.pop()
            elif len(key) == 1:
                buffer.append(key)
try:                
    kb.hook(on_key)
    kb.wait()
except KeyboardInterrupt:
    print("\nExiting...")