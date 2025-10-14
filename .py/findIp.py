from threading import Thread
from sys import stdout
import requests
def get(ip):
    stdout.write(f'\rchecking {ip}')
    url = f"http://{ip}:3000"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            stdout.write(f"\n{url}\n")
    except requests.exceptions.Timeout:
        pass
    except:
        stdout.write(f"\ncheck {ip}\n")
n8 = 187
add = int(input("Start N16 at: "))
threads = []
p = range(256)
n16 = add
for n24 in p:
    for n32 in p:
        t = Thread(target=get, args=(f"{n8}.{n16}.{n24}.{n32}",))
        t.start()
        threads.append(t)
for t in threads:
    t.join()