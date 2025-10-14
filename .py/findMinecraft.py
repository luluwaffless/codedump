from nbtlib import Compound, tag, load
from mcstatus import JavaServer
from os.path import expanduser
from datetime import datetime
from threading import Thread
from time import sleep
from sys import stdout
servers = load(expanduser("~\\AppData\\Roaming\\.minecraft\\servers.dat"))
def log(ip, s):
    try:
        iso = datetime.now().isoformat()
        text = f"----------------------------------------\n- IP: {ip}\n- Players ({s.players.online}/{s.players.max}):\n{'\n'.join(f'  - {player.name}' for player in s.players.sample)}\n- Version: {s.version.name}\n- Description: {s.motd.to_plain()}\n- Latency: {s.latency}ms\n[{iso}]\n"
        stdout.write(f'\n{text}----------------------------------------\n')
        with open('ips.log', 'a') as f:
            f.write(text)
        servers.get('servers').append(Compound({
            'name': tag.String(ip),
            'ip': tag.String(ip),
            'icon': tag.String(s.icon or ""),
            'hidden': tag.Byte(0)
        }))
        servers.save()
    except Exception as e:
        stdout.write(f"\n{e}\n")
def miningAway(ip):
    stdout.write(f'\r{ip}')
    try:
        r = JavaServer.lookup(f"{ip}:25565")
        s = r.status()
        log(ip, s)
    except:
        pass
n8 = 187
add = int(input("Start N16 at: "))
t = None
p = range(256)
for n16 in p:
    for n24 in p:
        for n32 in p:
            t = Thread(target=miningAway, args=(f"{n8}.{n16 + add}.{n24}.{n32}",))
            t.start()
            sleep(1/1000)
t.join()