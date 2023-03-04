import requests

url = "http://localhost:3000/"

async def getMoney(username, server):
    id = server + username
    money = await requests.get(url + "/" + id)
    return money

async def updateMoney(username, server, money):
    id = server + username
    await requests.post(url + "/" + id + "/" + money)