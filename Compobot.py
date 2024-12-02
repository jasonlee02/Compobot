import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
from database import JsonDB
import compost_game

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)


database = None

       
def init_db():
    global database
    if database is not None: return
    database = JsonDB("data.json")

# @client.event
# async def on_ready():
#    print(f'We have logged in as {client.user}')

@bot.command()
async def help_me(ctx):
    response = '''
       **Commands**
       **/balance**
       Shows how much money you have.
       **/cook**
       Enjoy a homecooked meal for $5.
       **/restaurant**
       Treat yourself and eat out for $15.
       **/compost**
       Use to composte your generated waste.
       **/trash**
       Use to trash your generated waste.
       **/beg**
       Broke? Earn some petty cash.
       **/gamble**
       Test your luck with a $50 buy in. Double it or lose it all!
       **/garden**
       Create a garden for $2 and gain a chance to earn money from your harvest!
       '''
    await ctx.send(response)

@bot.command()
async def beg(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.beg(user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def balance(ctx):
    init_db()
    user_money = database.get(str(ctx.author.id))
    await ctx.send(f"You have ${user_money}!")

@bot.command()
async def gamble(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.gamble(user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def garden(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.garden(user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def kill_me(ctx):
    await ctx.send("Kill yourself")

@bot.command()
async def cook(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.cook(user_id, user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def restaurant(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.restaurant(user_id, user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def compost(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.compost(user_id, user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

@bot.command()
async def trash(ctx):
    init_db()
    user_id = str(ctx.author.id)
    user_money = database.get(user_id)
    response, new_money = compost_game.trash(user_id, user_money)
    database.set(user_id, new_money)
    await ctx.send(response)

while True:
    try:
        bot.run(os.environ.get('DISCORD_TOKEN')) #put in .env later
    except RuntimeError:
        sys.exit(0)
    except:
        pass