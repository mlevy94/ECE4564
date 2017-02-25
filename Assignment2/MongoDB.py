cdimport pymongo
from pymongo import MongoClient

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

db = client.test_database

collection = db.test_collection

collection.delete_many({})

test = [{"author": "Hunter",
         "net": {"rx": 0, "tx": 0},
         "wlan0":{"rx": 708, "tx": 1192},
         "eth0":{ "rx": 0, "tx": 0},
         "cpu": 0.2771314211797171},
        {"author": "Clone2",
         "text": "100",
         "tags": ["mongodb", "python"]}]


collection_id = collection.insert_many(test)

collection.find_one_and_update({"author": "Hunter"})
findHigh(120, int(collection.find_one({"author": "Clone2"})["text"]))
print(collection.find_one({"author": "Clone2"})["text"])
print(collection.find({"author":"Hunter"}).count())


# placeholders
# cpu

# l0
# eth0
# wlan0


