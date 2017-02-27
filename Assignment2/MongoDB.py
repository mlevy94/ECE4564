import pymongo
from pymongo import MongoClient


class Client:
    def create_client(self):

        self.client = MongoClient('localhost', 27017)
        self.db = self.client.A2_database
        self.pi = self.db.pi_collection

    def mongo_insert(self, routing, js):
        pi_id = self.pi.insert_one({"Pi": routing, "info": js}).inserted_id

        cursor = self.pi.find({"Pi": routing})
        doc = next(self.pi.find({}).sort('info.cpu', pymongo.DESCENDING).limit(1))
        print(doc['info']['cpu'])
        doc = next( self.pi.find({}).sort('info.cpu', pymongo.ASCENDING).limit(1))
        print(doc['info']['cpu'])

        for interface, rates in js["net"].items():
            interString = interface
            for rate in rates:
                # grab min, max
                doc = next(self.pi.find({"Pi": routing}).sort("info.net.{}.{}".format(interface, rate), pymongo.ASCENDING).limit(1))
                print("{}: {}: min:{}".format(interface, rate, doc["info"]["net"][interface][rate]))
                doc = next(
                    self.pi.find({"Pi": routing}).sort("info.net.{}.{}".format(interface, rate), pymongo.DESCENDING).limit(
                        1))
                print("{}: {}: max:{}".format(interface, rate, doc["info"]["net"][interface][rate]))








if __name__ == "__main__":
    client = Client()
    client.create_client()
    client.mongo_insert('routing', {
        "net": {"lo": {"rx": 100, "tx": 100}, "wlan0": {"rx": 1000, "tx": 1000}, "eth0": {"rx": 100, "tx": 100}},
        "cpu": 0.00011797171})
