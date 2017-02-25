import pymongo
from pymongo import MongoClient

import json

def findHigh(num1, num2):
    if (num1 >= num2):
        High = num1
    else:
        High = num2
    print(High)


def findLow(num1, num2):
    if (num1 <= num2):
        Low = num1
    else:
        Low = num2
    print(Low)

client = MongoClient('localhost', 27017)

db = client.P2_database

pi1 = db.pi1_collection

lorx
lotx
wlanrx
wlantx
ethrx
ethtx
cputime


pi1.delete_many({})


info = ({"Pi": "pi1",
         "net": {"lo": {"rx": lorx, "tx": lotx },
         "wlan0": {"rx": wlanrx, "tx": wlantx},
         "eth0": {"rx": ethrx, "tx": ethtx}},
         "cpu": cputime})



pi1_id = pi1.insert_one(info).inserted_id





findHigh(120, int(pi1.find_one({"author": "Hunter"})["cpu"]))
print(pi1.find_one({"author": "Hunter"})["cpu"])
print(pi1.find({"author":"Hunter"}).count())


# placeholders
# cpu

# l0
# eth0
# wlan0


