import pymongo
from pymongo import MongoClient


class Client:

    global client
    global db
    global pi

    def create_client(self):

        client = MongoClient('localhost', 27017)
        db = client.A2_database
        pi = db.pi_collection

    def mongo_insert(self, routing, js):
        pi_id = pi.insert_one({"Pi":routing, "info":js}).inserted_id

        print(pi.find_one({"Pi": "pi1"})["cpu"])
        print(pi.find({"Pi": "pi1"}).count())

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
