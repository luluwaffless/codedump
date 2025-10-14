from pyautogui import moveTo, click
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

webbrowser.open("http://localhost")