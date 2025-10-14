from dotenv import load_dotenv
load_dotenv()
from os import environ
from datetime import datetime
from win32api import SetSystemTime as setTime
from requests import get
print("getting time...")
r = get("https://api.api-ninjas.com/v1/worldtime?timezone=Africa/Sao_Tome", headers={"X-Api-Key": environ.get("apininjas")})
print(r.json())
dt = datetime.fromisoformat(r.json()["datetime"])
timetuple =  (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond // 1000)
weekday = datetime(*timetuple).isocalendar()[2]
t = timetuple[:2] + (weekday,) + timetuple[2:]
print("updating time...")
setTime(*t)
print("done!")