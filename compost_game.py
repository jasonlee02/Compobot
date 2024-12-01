import random

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

cache = {}

def get_waste():
    randomNum = random.random()
    if randomNum < 0.4:
        return random.choice(commonCompost)
    elif randomNum < 0.8:
        return random.choice(commonTrash)
    elif randomNum < 0.9:
        return random.choice(rareCompost)
    else:
        return random.choice(rareTrash)
    


def beg(initial_money):
    new_money = initial_money + 1
    response = f"Some kind samaritan took pity on you. You now have ${new_money}."
    return response, new_money

def gamble(initial_money):
    if initial_money < 50:
        return "You don't have enough money to gamble.", initial_money

    r = random.random()
    if r < .75:
        new_money = initial_money - 50
        response = f"Tough luck! You lost $50. You now have ${new_money}."
        return response, new_money
    else:
        new_money = initial_money +100
        response = f"Congratulations! You won $100. You now have ${new_money}."
        return response, new_money
    
def garden(initial_money):
    if initial_money < 2:
        return "You don't have enough money to start a garden.", initial_money

    new_money = initial_money - 2
    r = random.random()
    if r < .001:
        new_money += 100
        return "Not sure how this happened... you harvested GOLD!!! You earned $100!", new_money
    elif r < .1001:
        return "Looks like you didn't compost right... you harvested nothing.", new_money
    elif r < .2801:
        new_money += 5
        return "Looks like you're suited to gardening! You harvested a tomato and earned $5!", new_money
    elif r < .4601:
        new_money += 5
        return "Looks like you're suited to gardening! You harvested a carrot and earned $5!", new_money
    elif r < .6401:
        new_money += 5
        return "Looks like you're suited to gardening! You harvested a potato and earned $5!", new_money
    elif r < .8201:
        new_money += 10
        return "Peak composting skills! You harvested a squash and earned $10!", new_money
    else:
        new_money += 15
        return "Peak composting skills! You harvested a pumpkin and earned $15!", new_money


def cook(user_id, initial_money):
    if initial_money < 5:
        return "You can't afford this meal.", initial_money
    
    new_money = initial_money - 5
    waste = get_waste()
    cache[user_id] = waste

    return f"After enjoying a homecooked meal, your waste generated is {waste}. Is this compostable, or trash?", new_money

def restaurant(user_id, initial_money):
    if initial_money < 15:
        return "You can't afford this meal.", initial_money
    
    new_money = initial_money - 15
    waste = get_waste()
    cache[user_id] = waste
    
    return f"After treating yourself to a meal out, your generated waste is {waste}. Is this compostable, or trash?", new_money

def compost(user_id, initial_money):
    if user_id not in cache:
        return "You have no waste! Cook or go to a restaurant to generate waste.", initial_money
    
    waste = cache[user_id]
    del cache[user_id]

    if waste in commonCompost or waste in rareCompost:
        money_earned = 10 if waste in commonCompost else 25
        new_money = initial_money + money_earned
        return f"Correct! You earned ${money_earned}!", new_money
    else:
        return "Wrong. You didn't earn any money.", initial_money

def trash(user_id, initial_money):
    if user_id not in cache:
        return "You have no waste! Cook or go to a restaurant to generate waste.", initial_money
    
    waste = cache[user_id]
    del cache[user_id]

    if waste in commonTrash or waste in rareTrash:
        money_earned = 10 if waste in commonTrash else 25
        new_money = initial_money + money_earned
        return f"Correct! You earned ${money_earned}!", new_money
    else:
        return "Wrong. You didn't earn any money.", initial_money