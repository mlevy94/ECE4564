import pymongo
import time
from pymongo import MongoClient
from pymongo import errors


class Client:
    
    def __init__(self):
        self.client = None
        while self.client is None:
            try:
                self.client = MongoClient('netapps.ece.vt.edu', 27017)
            except errors.ConnectionFailure:
                print("Failed to connect to MongoDB. Retrying in 1 second...")
                time.sleep(1)
        self.db = self.client.A2_database
        self.pi = self.db.pi_collection

    def mongo_insert(self, routing, js):
        pi_id = self.pi.insert_one({"Pi": routing, "info": js}).inserted_id

        print("\n{}:".format(routing))
        print("cpu: {} [Hi: {}, Lo: {}]".format(
            js["cpu"],
            next(self.pi.find({}).sort('info.cpu', pymongo.DESCENDING).limit(1))['info']['cpu'],
            next(self.pi.find({}).sort('info.cpu', pymongo.ASCENDING).limit(1))['info']['cpu'],
        ))

        for interface, rates in js["net"].items():
            rateStrings = []
            for rate in rates:
                rateStrings.append("{}={} B/s [Hi: {} B/s, Lo: {} B/s]".format(rate, js["net"][interface][rate],
                next(self.pi.find({"Pi": routing}).sort("info.net.{}.{}".format(interface, rate), pymongo.ASCENDING).limit(1))["info"]["net"][interface][rate],
                next(self.pi.find({"Pi": routing}).sort("info.net.{}.{}".format(interface, rate), pymongo.DESCENDING).limit(1))["info"]["net"][interface][rate],
                ))
            print("{}: {}".format(interface, ", ".join(rateStrings)))









if __name__ == "__main__":
    client = Client()
    client.create_client()
    client.mongo_insert('routing', {
        "net": {"lo": {"rx": 100, "tx": 100}, "wlan0": {"rx": 1000, "tx": 1000}, "eth0": {"rx": 100, "tx": 100}},
        "cpu": 0.00011797171})
