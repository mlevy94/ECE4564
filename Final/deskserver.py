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
                self.desks.append(desk)
                payload = json.dumps(desk)
                r = requests.post(self.url + 'desk', json=json.loads(payload))

    def update(self, old_beacon, new_beacon, ip, occupied):
        updated_desk = {'beacon': new_beacon, 'ip': ip, 'occupied': occupied}
        payload = json.dumps(updated_desk)
        r = requests.put(self.url + 'desk/' + str(old_beacon), json=json.loads(payload))
        return r.ok

    def add_desk(self, beacon, ip):
        new_desk = {'beacon' : beacon, 'ip' : ip}
        payload = json.dumps(new_desk)
        r = requests.post(self.url + 'desk', json=json.loads(payload))
        return r.ok

    def remove_desk(self, beacon):
        r = requests.delete(self.url + 'desk/' + str(beacon))
        return r.ok

    def get_desk(self, beacon):
        r = requests.get(self.url + 'desk/' + str(beacon))
        desk = r.json()
        return desk

    def get_in_use(self, beacon):
        desk = self.get_desk(beacon)
        return desk['desk']['occupied']

    def set_in_use(self, beacon, occupied):
        use = {'occupied' : occupied}
        payload = json.dumps(use)
        r = requests.put(self.url + 'desk/use/' + str(beacon), json=json.loads(payload))
        return r.ok

if __name__ == '__main__':

    ds = DeskServer()
