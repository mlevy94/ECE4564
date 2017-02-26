import pymongo
from pymongo import MongoClient

import json








client = MongoClient('localhost', 27017)

db = client.P2_database

pi1 = db.pi1_collection
s = '{"Pi": "pi1","net": {"lo": {"rx": 0,"tx": 0},"wlan0":{"rx": 708,"tx": 1192},"eth0": {"rx": 0,"tx": 0}},"cpu": 0.8393824}'
str = json.loads(s)
identity = str["Pi"]
lorx = str["net"]["lo"]["rx"]
lotx = str["net"]["lo"]["tx"]
wlanrx = str["net"]["wlan0"]["rx"]
wlantx = str["net"]["wlan0"]["tx"]
ethrx = str["net"]["eth0"]["rx"]
ethtx = str["net"]["eth0"]["tx"]
cputime = str["cpu"]




info = ({"Pi": identity,
         "net": {
              "lo": {"rx": lorx , "tx": lotx},
              "wlan0": {"rx": wlanrx, "tx": wlantx},
              "eth0": {"rx": ethrx, "tx": ethtx}},
         "cpu": cputime})

#pi1_id = pi1.insert_one(info).inserted_id

print(pi1.find_one({"Pi": "pi1"})["cpu"])
print(pi1.find({"Pi": "pi1"}).count())

for doc in pi1.find().sort('cpu', pymongo.DESCENDING):
    print(doc)
    break
