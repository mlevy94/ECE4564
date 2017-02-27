import pymongo
from pymongo import MongoClient

import json

client = MongoClient('localhost', 27017)

db = client.A2_database

pi = db.pi_collection
s = '{"routing": "pi1","net": {"lo": {"rx": 0,"tx": 0},"wlan0":{"rx": 708,"tx": 1192},"eth0": {"rx": 0,"tx": 0}},"cpu": 0.8393824}'
str = json.loads(s)
identity = str["routing"]
lorx = str["net"]["lo"]["rx"]
lotx = str["net"]["lo"]["tx"]
wlanrx = str["net"]["wlan0"]["rx"]
wlantx = str["net"]["wlan0"]["tx"]
ethrx = str["net"]["eth0"]["rx"]
ethtx = str["net"]["eth0"]["tx"]
cputime = str["cpu"]

pi.delete_many({})
info = ({"Pi": identity,
         "net": {
             "lo": {"rx": lorx, "tx": lotx},
             "wlan0": {"rx": wlanrx, "tx": wlantx},
             "eth0": {"rx": ethrx, "tx": ethtx}},
         "cpu": cputime})

pi_id = pi.insert_one(info).inserted_id

print(pi.find_one({"Pi": "pi1"})["cpu"])
print(pi.find({"Pi": "pi1"}).count())

if (identity == 'pi1'):

    for doc in pi.find().sort('cpu', pymongo.DESCENDING):
        print('hi: {}'.format(doc["cpu"]))
        break

    for doc in pi.find().sort('cpu', pymongo.ASCENDING):
        print('lo: {}'.format(doc["cpu"]))
        break
