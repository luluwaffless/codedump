from settings import bulb, led
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal
from json import loads
import webbrowser

class Dps(BaseModel):
    switch: bool | None = None
    mode: Literal["colour", "white", "scene"] | None = None
    brightness: int | None = None
    temperature: int | None = None
    colour: str | None = None
    scene: str | None = None
    timer: int | None = None

app = FastAPI()
@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/{file}")
async def file(file: str):
    return FileResponse(f"static/{file}")

@app.get("/icons/{file}")
async def icons(file: str):
    return FileResponse(f"static/icons/{file}")
    
@app.websocket("/ws/{device}")
async def ws(websocket: WebSocket, device: str):
    if device != "bulb" and device != "led":
        await websocket.close(code=1003, reason="Invalid device")
    await websocket.accept()
    if device == "bulb":
        state = bulb.state()
    elif device == "led":
        state = led.state()
    await websocket.send_json(state)
    try:
        while True:
            request = await websocket.receive_text()
            if request == "state":
                if device == "bulb":
                    state = bulb.state()
                elif device == "led":
                    state = led.state()
                await websocket.send_json(state)
            else:
                data = loads(request)
                try:
                    dps = Dps(**data)
                except Exception as e:
                    print(e)
                    continue
                dps_dict = {
                    "20": dps.switch if isinstance(dps.switch, bool) else None,
                    "21": dps.mode if dps.mode else None,
                    "22": dps.brightness if dps.brightness else None,
                    "23": dps.temperature if dps.temperature else None,
                    "24": dps.colour if dps.colour else None,
                    "25": dps.scene if dps.scene else None,
                    "26": dps.timer if dps.timer else None
                }
                if device == "bulb":
                    bulb.set_multiple_values(dps_dict, nowait=True)
                elif device == "led":
                    led.set_multiple_values(dps_dict, nowait=True)
    except WebSocketDisconnect:
        pass

webbrowser.open("https://localhost")