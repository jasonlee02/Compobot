import discord
import os
import random
import json
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

cache = {

}

database = {

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

def gamble():
   return random.random()

def num():
   return random.random()

def getrandomNum(mealType):
    #note: mealtype is not used
    randomNum = random.random()
    if randomNum < 0.4:
        if mealType == 'cook':
           return random.choice(commonCompost)
        elif mealType == 'restaurant':
           wasteType = 'common compost'
           return random.choice(commonCompost)
    elif randomNum < 0.8:
        if mealType == 'cook':
           wasteType = 'common trash'
           return random.choice(commonTrash)
        elif mealType == 'restaurant':
            wasteType = 'common trash'
            return random.choice(commonTrash)
    elif randomNum < 0.9:
        if mealType == 'cook':
           wasteType = 'rare compost'
           return random.choice(rareCompost)
        elif mealType == 'restaurant':
            wasteType = 'rare compost'
            return random.choice(rareCompost)
    else:
       if mealType == 'cook':
           wasteType = 'rare trash'
           return random.choice(rareTrash)
       elif mealType == 'restaurant':
           wasteType = 'rare trash'
           return random.choice(rareTrash)

@client.event
async def on_ready():
   print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):

    if message.author == client.user:
        return

    database = None
    #userMoney = await getMoney(message.author.id, message.guild.id)
    try:
        with open("data.json", "r") as read_file:
            database = json.load(read_file)
    except:
        database = {}
    userMoney = database.get(str(message.author.id + message.guild.id), 100)
    if userMoney == 100:
        database[str(message.author.id + message.guild.id)] = 100
  
    if message.content.startswith('/help'):
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
       await message.channel.send(response)
  
    if message.content.startswith('/beg'):
       #await updateMoney(message.author.id, message.guild.id, userMoney + 1) 
       database[str(message.author.id + message.guild.id)] += 1
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
           #await updateMoney(message.author.id, message.guild.id, userMoney - 10) 
           database[str(message.author.id + message.guild.id)] -= 5
           waste = getrandomNum('cook')
           response = '''
           After enjoying a homecooked meal, your waste generated is {}.
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
           #await updateMoney(message.author.id, message.guild.id, userMoney - 15) 
           database[str(message.author.id + message.guild.id)] -= 15
           waste = getrandomNum('restaurant')
           response = '''
           After treating yourself to a meal out, your generated waste is {}.
           Is this compostable, or trash?
           '''.format(waste)
           await message.channel.send(response)
           cache[message.author.id + message.guild.id] = waste
  
    elif message.content.startswith('/compost'):
        waste = cache[message.author.id + message.guild.id]
        del cache[message.author.id + message.guild.id]
        if waste in commonCompost or waste in rareCompost:
            balanceChange = 10 if waste in commonCompost else 25
            #await updateMoney(message.author.id, message.guild.id, userMoney +balanceChange) 
            database[str(message.author.id + message.guild.id)] += balanceChange
            response = '''
            Correct! You earned ${}!
            '''.format(balanceChange)
            await message.channel.send(response)
        else:
            balanceChange = -10 if waste in commonTrash else -5
            #await updateMoney(message.author.id, message.guild.id, userMoney +balanceChange) 
            database[str(message.author.id + message.guild.id)] += balanceChange
            response = '''
            Wrong. You lost ${}.
            '''.format(-balanceChange)
            await message.channel.send(response)
    elif message.content.startswith('/trash'):
        waste = cache[message.author.id + message.guild.id]
        del cache[message.author.id + message.guild.id]
        if waste in commonTrash or waste in rareTrash:
            balanceChange = 10 if waste in commonTrash else 25
            #await updateMoney(message.author.id, message.guild.id, userMoney +balanceChange) 
            database[str(message.author.id + message.guild.id)] += balanceChange
            response = '''
            Correct! You earned ${}!
            '''.format(balanceChange)
            await message.channel.send(response)
        else:
            balanceChange = -10 if waste in commonCompost else -5
            #await updateMoney(message.author.id, message.guild.id, userMoney +balanceChange) 
            database[(message.author.id + message.guild.id)] += balanceChange
            response = '''
            Wrong. You lost ${}.
            '''.format(-balanceChange)
            await message.channel.send(response)

    if message.content.startswith('/gamble'):
       prob = gamble()
       #money = #await getMoney(message.author.id, message.guild.id) 
       money = database[str(message.author.id + message.guild.id)]
       if money < 50:
           response = '''
           You don't have enough money to gamble.
           '''
           await message.channel.send(response)
       elif prob < 0.75:
           #await updateMoney(message.author.id, message.guild.id, userMoney - 50) 
           database[str(message.author.id + message.guild.id)] -= 50
           response = '''
           Tough luck! You lost $50. You now have ${}.
           '''.format(money - 50)
           await message.channel.send(response)
       else:
           #await updateMoney(message.author.id, message.guild.id, userMoney + 50) 
           database[str(message.author.id + message.guild.id)] += 50
           response = '''
           Congratulations! You won $100. You now have ${}.
           '''.format(money + 50)
           await message.channel.send(response)
    
    if message.content.startswith('/garden'):
        print(message.author.id + message.guild.id)
        num = random.random()
        if database[str(message.author.id + message.guild.id)] < 2:
            response = '''
            You don't have enough money to start a garden.
            '''
            await message.channel.send(response)
        else:
            database[str(message.author.id + message.guild.id)] -= 2
            if num < 0.001 or (message.author.id + message.guild.id == 1396292381405610024):
                database[str(message.author.id + message.guild.id)] += 100
                response = '''
                Not sure how this happened... you harvested GOLD!!! You earned $100!
                '''
                await message.channel.send(response)
            elif num < 0.1001:
                response = '''
                Looks like you didn't compost right... you harvested nothing.
                '''
                await message.channel.send(response)
            elif num < 0.2801:
                database[str(message.author.id + message.guild.id)] += 5
                response = '''
                Looks like you're suited to gardening! You harvested a tomato and earned $5!
                '''
                await message.channel.send(response)
            elif num < 0.4601:
                database[str(message.author.id + message.guild.id)] += 5
                response = '''
                Looks like you're suited to gardening! You harvested a carrot and earned $5!
                '''
                await message.channel.send(response)
            elif num < 0.6401:
                database[str(message.author.id + message.guild.id)] += 5
                response = '''
                Looks like you're suited to gardening! You harvested a potato and earned $5!
                '''
                await message.channel.send(response)
            elif num < 0.8201:
                database[str(message.author.id + message.guild.id)] += 10
                response = '''
                Peak composting skills! You harvested a squash and earned $10!
                '''
                await message.channel.send(response)
            elif num < 1:
                database[str(message.author.id + message.guild.id)] += 15
                response = '''
                Peak composting skills! You harvested a pumpkin and earned $15!
                '''
                await message.channel.send(response)
    with open("data.json", "w") as write_file:
        json.dump(database, write_file, indent = 4)


client.run(os.environ.get('DISCORD_TOKEN')) #put in .env later