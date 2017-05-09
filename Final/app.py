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
    uuid = request.form.get('uuid', None)
    height = request.form.get('height', None)
    user = request.form.get('user', None)
    desk = desks.find_one({'_id' : uuid}) 
    if desk is None or desk['occupied']:
        return ''
    desks.update_one({'_id' : uuid}, { '$set': {'user': user, 'occupied' : True}})
    client = SockClient(desk['ip'])
    client.send(json.dumps({'height':height}))
    return ''

@app.route('/exit', methods=['POST'])
def exit_desk():
    user = request.form.get('user', None)
    uuid = request.form.get('uuid', None)
    desk = desks.find_one({'_id': uuid})
    if desk['user'] != user:
        return ''
    desks.update_one({'_id': uuid}, {'$set': {'user': None, 'occupied': False}})
    return ''

app.run(host='0.0.0.0', debug=True)
