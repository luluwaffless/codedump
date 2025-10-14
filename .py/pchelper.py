from dotenv import load_dotenv
load_dotenv()
from os import environ
from PIL.ImageGrab import grab
from io import BytesIO
import discord
import socket
import psutil
import GPUtil
import requests
intents = discord.Intents.default()
intents.message_content = True # make sure your bot has message content intent
client = discord.Client(intents=intents)

def get_public_ip():
    try:
        return requests.get("https://ipinfo.io/json").json()['ip']
    except:
        return "Unavailable"

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "Unavailable"

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

def get_ram_usage():
    mem = psutil.virtual_memory()
    return {
        "percent": mem.percent,
        "used_gb": mem.used / (1024 ** 3),
        "total_gb": mem.total / (1024 ** 3)
    }

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        info = []
        for gpu in gpus:
            info.append({
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load * 100,
                "temp": gpu.temperature,
                "mem_used": gpu.memoryUsed,
                "mem_total": gpu.memoryTotal
            })
        return info
    except:
        return []
 
@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    user = await client.fetch_user(environ.get('discordid'))
    dm = await user.create_dm()
    await dm.send("hallo!!")
@client.event
async def on_message(message):
    if message.content == 'status':
        image = grab((0, 0, 1920, 1080))
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        ram = get_ram_usage()
        gpus = get_gpu_info()
        await message.reply(content=f"Public IP: ||`{get_public_ip()}`||\nLocal IP: `{get_local_ip()}`\nCPU Usage: {get_cpu_usage():.1f}%\nRAM Usage: {ram['percent']:.1f}% ({ram['used_gb']:.1f} / {ram['total_gb']:.1f} GB)\n{''.join((f"GPU {gpu['id']}: {gpu['name']}\n- Load: {gpu['load']:.1f}%\n- Temp: {gpu['temp']} °C\n- VRAM: {gpu['mem_used']} / {gpu['mem_total']} MB" for gpu in gpus) if gpus else "No GPU detected (or NVIDIA drivers not installed)")}", file=discord.File(buf, filename="image.png"))
client.run(environ.get('discord1'))