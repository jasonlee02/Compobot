import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/balance'):
        await message.channel.send('Hello!')

    if message.content.startswith('/cook'):
        await message.channel.send('Hello!')

client.run(os.getenv('DISCORD_TOKEN')) #put in .env later