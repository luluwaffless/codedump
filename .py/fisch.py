from dotenv import load_dotenv
load_dotenv()
from os import environ
import discord
import webbrowser
import re
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == 1302125367712026715:
        print(f"[{message.author.name}] {message.content}")
        try:
            servers = re.findall(r"(https://www\.roblox\.com/share\?code=[^\s]+|https://www\.roblox\.com/games/16732694052/Fisch\?privateServerLinkCode=[^\s]+)", message.content)
            webbrowser.open(servers[0])
        except:
            pass

client.run(environ.get('discord2'))