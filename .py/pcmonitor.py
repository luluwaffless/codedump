import os
import socket
import psutil
import GPUtil
import requests
import time

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
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    while True:
        public_ip = get_public_ip()
        local_ip = get_local_ip()
        cpu_usage = get_cpu_usage()
        ram = get_ram_usage()
        gpus = get_gpu_info()
        clear()
        print(f"Public IP: {public_ip}\nLocal IP: {local_ip}\nCPU Usage: {cpu_usage:.1f}%\nRAM Usage: {ram['percent']:.1f}% ({ram['used_gb']:.1f} / {ram['total_gb']:.1f} GB)\n{''.join((f"GPU {gpu['id']}: {gpu['name']}\n- Load: {gpu['load']:.1f}%\n- Temp: {gpu['temp']} °C\n- VRAM: {gpu['mem_used']} / {gpu['mem_total']} MB" for gpu in gpus) if gpus else "No GPU detected (or NVIDIA drivers not installed)")}")
        time.sleep(30)
        print('\n...')
except KeyboardInterrupt:
    print("\nExiting...")