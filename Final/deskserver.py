import json
import io
import requests
import os
import datetime


class DeskServer:

    desks = []
    users = []
    url = 'http://0.0.0.0:5000/'

    def __init__(self):
        if os.path.isfile('./data.json'):
            json_data = open('data.json').read()
            self.data = json.loads(json_data)
            for desk in self.data['desks']:
                self.desks.append(self, desk)
                payload = json.dumps(desk)
                r = requests.post(self.url + 'desk', json=json.loads(payload))

if __name__ == '__main__':

    ds = DeskServer()
