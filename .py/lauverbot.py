# codedump note: never finished this and i think its broken now
from dotenv import load_dotenv
load_dotenv()
from os import environ
from TikTokApi import TikTokApi
from instagrapi import Client
import asyncio
import logging
import discord
bot = discord.Client(intents=discord.Intents.default())
print("logging in instagram...")
insta = Client()
insta.login(environ.get("ig"), environ.get("igpass"))
print("logged in!")
ms_token = environ.get("ms_token")
username = "laufey"
userid = insta.user_id_from_username("laufey")
lastVideos = []
lastMedias = []

async def get_video():
    global username
    global lastVideos
    async with TikTokApi(logging_level=logging.INFO) as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        ls = []
        async for video in api.user(username=username).videos(count=1):
            ls.append(int(video.id))
        for id in ls:
            if not id in lastVideos:
                print(f"new video! https://www.tiktok.com/@{username}/{id}")
                lastVideos.insert(0, id)
                if len(lastVideos) > 32:
                    lastVideos.pop()
async def get_posts():
    global userid
    global lastMedias
    ls = []
    for media in insta.user_medias(userid, 32):
        ls.append(media.code)
    for code in ls:
        if not code in lastMedias:
            print(f"new post! https://www.instagram.com/p/{code}/")
            lastMedias.insert(0, id)
            if len(lastMedias) > 32:
                lastMedias.pop()
@bot.event
async def on_ready():
    print(f'logged in as {bot.user}!')
    print("starting tasks...")
    while True:
        await get_video()
        await get_posts()
        await asyncio.sleep(30)
print("logging in discord...")
bot.run(environ.get('discord4'))