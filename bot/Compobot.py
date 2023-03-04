import discord
import os
import random
from api import getMoney
from api import updateMoney
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

cache = {

}

commonCompost = [
   'a banana peel', 'an apple core', 'tea leaves', 'coffee grounds', 'a paper egg carton', 'a napkin'
]
rareCompost = [
   'a cereal box', 'egg shells', 'spoiled almond milk', 'peanut shells', 'a wine cork'
]
commonTrash = [
   'a pizza box', 'a plastic wrapper', 'a styrofoam cup', 'a plastic straw', 'butter', 'bones'
]
rareTrash = [
   'a block of cheese', 'eggs', 'meat', 'peanut butter', 'dessert', 'cooked rice'
]

def getrandomNum(mealType):
    #note: mealtype is not used
    randomNum = random.random()
    waste = None
    if randomNum < 0.4:
        if mealType == 'cook':
           waste = random.choice(commonCompost)
        elif mealType == 'restaurant':
           wasteType = 'common compost'
           waste = random.choice(commonCompost)
    elif randomNum < 0.8:
        if mealType == 'cook':
           wasteType = 'common trash'
           waste = random.choice(commonTrash)
        elif mealType == 'restaurant':
            wasteType = 'common trash'
            waste = random.choice(commonTrash)
    elif randomNum < 0.9:
        if mealType == 'cook':
           wasteType = 'rare compost'
           waste = random.choice(rareCompost)
        elif mealType == 'restaurant':
            wasteType = 'rare compost'
            waste = random.choice(rareCompost)
    else:
       if mealType == 'cook':
           wasteType = 'rare trash'
           waste = random.choice(rareTrash)
       elif mealType == 'restaurant':
           wasteType = 'rare trash'
           waste = random.choice(rareTrash)
    return waste

@client.event
async def on_ready():
   print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    userMoney = await getMoney(message.author.id, message.guild.id)
  
    if message.content.startswith('/help'):
       response = '''
       **Commands**
       **/balance**
       Shows how much money you have.
       **/cook**
       Enjoy a homecooked meal for $10.
       **/restaurant**
       Treat yourself and eat out for $15.
       **/compost**
       Use to composte your generated waste.
       **/trash**
       Use to trash your generated waste.
       **/beg**
       Broke? Earn some petty cash.
       '''
       await message.channel.send(response)
  
    if message.content.startswith('/beg'):
       await updateMoney(message.author.id, message.guild.id, userMoney + 1) 
       response = '''
       Some kind samaritan took pity on you. You now have ${}.
       '''.format(userMoney + 1)
       await message.channel.send(response)


    if message.content.startswith('/balance'):
       response = '''
       You have ${}!
       '''.format(userMoney)
       await message.channel.send(response)
  
    elif message.content.startswith('/cook'):
       if userMoney < 10:
           response = '''
           You can't afford this meal.
           '''
           await message.channel.send(response)
       else:
           await updateMoney(message.author.id, message.guild.id, userMoney - 10) 
           waste = getrandomNum('compost')
           response = '''
           After enjoying a homecooked meal, your waste generated is ${}.
           Is this compostable, or trash?
           '''.format(waste)
           await message.channel.send(response)
           cache[message.author.id + message.guild.id] = waste
      
    elif message.content.startswith('/restaurant'):
       if userMoney < 15:
           response = '''
           You can't afford this meal.
           '''
           await message.channel.send(response)
       else:
           await updateMoney(message.author.id, message.guild.id, userMoney - 15) 
           waste = getrandomNum('restaurant')
           response = '''
           After treating yourself to a meal out, your generated waste is ${}.
           Is this compostable, or trash?
           '''.format(waste)
           await message.channel.send(response)
           cache[message.author.id + message.guild.id] = waste
  
    elif message.content.startswith('/compost'):
        waste = cache[message.author.id + message.guild.id]
        del cache[message.author.id + message.guild.id]
        if waste in commonCompost or waste in rareCompost:
            balanceChange = 10 if waste in commonCompost else 25
            response = '''
            Correct! You earned ${}!
            '''.format(balanceChange)
            await message.channel.send(response)
        else:
            balanceChange = -10 if waste in commonTrash else -5
            response = '''
            Wrong. You lost ${}.
            '''.format(-balanceChange)
            await message.channel.send(response)
    elif message.content.startswith('/trash'):
        waste = cache[message.author.id + message.guild.id]
        del cache[message.author.id + message.guild.id]
        if waste in commonTrash or waste in rareTrash:
            balanceChange = 10 if waste in commonTrash else 25
            response = '''
            Correct! You earned ${}!
            '''.format(balanceChange)
            await message.channel.send(response)
        else:
            balanceChange = -10 if waste in commonCompost else -5
            response = '''
            Wrong. You lost ${}.
            '''.format(-balanceChange)
            await message.channel.send(response)


client.run(os.getenv('DISCORD_TOKEN')) #put in .env later