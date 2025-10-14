from dotenv import load_dotenv
load_dotenv()
from os import environ
from pytesseract import image_to_string
from PIL.ImageGrab import grab
from keyboard import send
from io import BytesIO
from re import sub
import discord
coins = int(input('how many coins do you have atm?\n> '))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    user = await client.fetch_user(environ.get('discordid'))
    dm = await user.create_dm()
    await dm.send("hallo!!")
@client.event
async def on_message(message):
    if message.content == 'check':
        global coins
        image = grab((1752, 114, 1854, 127)).convert('L')
        try:
            newAmount = int(sub(r'\D', '', image_to_string(image)))
            await message.reply(f'you have {newAmount:,} coins (**{"+" if newAmount >= coins else "-"}{abs(newAmount - coins):,}** since last check)')
            coins = newAmount
        except ValueError:
            buf = BytesIO()
            image.save(buf, format='PNG')
            buf.seek(0)
            await message.reply(f'uhh smth wrong with the OCR can u read this?\ncurrent count: {coins}', file=discord.File(buf, filename="image.png"))
    elif message.content == 'screenshot':
        image = grab((0, 0, 1920, 1080))
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        await message.reply(file=discord.File(buf, filename="image.png"))
    elif message.content == 'combo':
        send('ctrl+shift+c')
        await message.reply('done')
    elif message.content.startswith('set'):
        newAmount = int(sub(r'\D', '', message.content.split(' ')[1]))
        await message.reply(f'you have {newAmount:,} coins (**{"+" if newAmount >= coins else "-"}{abs(newAmount - coins):,}** since last check)')
        coins = newAmount
    elif message.content == 'ping':
        await message.reply('pong')
client.run(environ.get('discord1'))