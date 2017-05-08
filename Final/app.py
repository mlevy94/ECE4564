#!flask/bin/python
from flask import Flask, abort, make_response, request
import json
from pymongo import MongoClient
from sockcomm import SockClient

app = Flask(__name__)

db_client = MongoClient('localhost', 27017)

desks = db_client.A2_database.desk

@app.route('/enter', methods=['POST'])
def enter():
    uuid = request.args.get('uuid', None)
    height = request.args.get('height', None)
    user = request.args.get('user', None)
    desk = desks.findOne({'_id' : uuid})
    if desk['occupied']:
        return
    desks.updateOne({'_id' : uuid}, { '$set': {'user': user, 'occupied' : True}})
    client = SockClient(desk['ip'])
    client.send(json.dumps({'height':height}))

@app.route('/exit', methods=['POST'])
def exit_desk():
    user = request.args.get('user', None)
    uuid = request.args.get('uuid', None)
    desk = desks.findOne({'_id': uuid})
    if desk['user'] != user:
        return
    desks.updateOne({'_id': uuid}, {'$set': {'user': None, 'occupied': False}})
