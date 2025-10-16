from pyautogui import moveTo, click, press
from fastapi import FastAPI
from fastapi.responses import FileResponse
import webbrowser

CLICK = (1797, 913) # skip button location

app = FastAPI()
@app.get("/")
async def root():
    return FileResponse("index.html")
    
@app.post("/skip")
async def skip():
    moveTo(CLICK)
    click(CLICK)
    return 200

@app.post("/left")
async def left():
    press("left")
    return 200

@app.post("/right")
async def right():
    press("right")
    return 200

@app.post("/space")
async def space():
    press("space")
    return 200

webbrowser.open("http://localhost")