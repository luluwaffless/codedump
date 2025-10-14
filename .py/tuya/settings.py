from dotenv import load_dotenv
load_dotenv()
from os import environ
from tinytuya import BulbDevice
led = BulbDevice(environ.get("ledid"), environ.get("ledip"), environ.get("ledkey"))
bulb = BulbDevice(environ.get("bulbid"), environ.get("bulbip"), environ.get("bulbkey"))
led.set_version(3.3)
bulb.set_version(3.3)
__all__ = [led, bulb]