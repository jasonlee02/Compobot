import requests

url = "ec2-18-222-108-213.us-east-2.compute.amazonaws.com/:3000"

async def getMoney(username, server):
    id = server + username
    money = 0
    try:
        with requests.session() as session:
            money = session.get(url + "/" + str(id))
            print(money.json())
        return money.json()['money']
    except:
        return 100 # starting balance

async def updateMoney(username, server, money):
    id = server + username
    requests.post(url + "/" + str(id) + "/" + str(money))