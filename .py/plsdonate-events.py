from dotenv import load_dotenv
load_dotenv()
from os import environ
import requests
import discord
import json
import re
client = discord.Client()
webhook = "https://discord.com/api/webhooks/1247406991479935047/lmnoIv9zfr-8C9vQD3CzuZZ6cHjzg03FuvtPCjF1PfLwKfzZrusQgrC0xLflJ8oH31wP"

def format(urls):
    return '\n'.join(f'- {url}' for url in urls)

def get(text):
    url_regex = r'(https?://[^\s$.?#].[^\s]*)'
    urls = re.findall(url_regex, text)
    new_text = re.sub(url_regex, '<link>', text)
    return new_text, format(urls)

def send(content):
    data = json.dumps({"content": content})
    requests.post(webhook, headers={'Content-Type': 'application/json'}, data=data)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id == 951137480592212048:
        new_text, urls = get(message.content)
        send(f"# sent by <@{message.author.id}>:\n```\n{new_text}\n```\n## links:\n{urls}\n||@everyone||")

client.run(environ.get('discord2'))