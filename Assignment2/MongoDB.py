import pymongo
from pymongo import MongoClient


class Client:



    def create_client(self):

        self.client = MongoClient('localhost', 27017)
        self.db = self.client.A2_database
        self.pi = self.db.pi_collection

    def mongo_insert(self, routing, js):
        pi_id = self.pi.insert_one({"Pi":routing, "info":js}).inserted_id


        print(self.pi.find().sort('Pi.cpu', pymongo.ASCENDING))
        cursor = self.pi.find({'Pi': routing})
        
        # net stats
        for interface, rates in js["net"].items():
            interString = interface
            for rate in rates:
                # grab min, max
                interString += blah
            print(interString)

        # if (identity == 'pi1'):
        #
        #     for doc in pi.find().sort('cpu', pymongo.DESCENDING):
        #         print('hi: {}'.format(doc["cpu"]))
        #         break
        #
        #     for doc in pi.find().sort('cpu', pymongo.ASCENDING):
        #         print('lo: {}'.format(doc["cpu"]))
        #         break
        #
        #     for doc in pi.find().sort('net', pymongo.ASCENDING).items():
        #         for doc2 in pi.find().sort(doc, pymongo.ASCENDING).items():
        #             print('lo: {}'.format(doc2['tx']))
        #             print('hi: {}'.format(doc2['rx']))
        #             break
        #
        # if (identity == 'pi2'):
        #
        #     for doc in pi.find().sort('cpu', pymongo.DESCENDING):
        #         print('hi: {}'.format(doc["cpu"]))
        #         break
        #
        #     for doc in pi.find().sort('cpu', pymongo.ASCENDING):
        #         print('lo: {}'.format(doc["cpu"]))
        #         break
        #
        #     for doc in pi.find().sort('net', pymongo.ASCENDING).items():
        #         for doc2 in pi.find().sort(doc, pymongo.ASCENDING).items():
        #             print('lo: {}'.format(doc2['tx']))
        #             print('hi: {}'.format(doc2['rx']))
        #             break


if __name__ == "__main__":
    client = Client()
    client.create_client()
    client.mongo_insert('routing','{"net": { "lo": { "rx": 0, "tx": 0 }, "wlan0": { "rx": 708, "tx": 1192 }, "eth0": { "rx": 0, "tx": 0 } }, "cpu": 0.2771314211797171}')

