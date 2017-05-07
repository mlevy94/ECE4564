#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import io
import os

app = Flask(__name__)

desks = []

@app.route('/')
def index():
   return "Hello, World!"
	
@app.route('/desk', methods=['GET'])
def get_desks():
    return jsonify({'desks': desks})
	
@app.route('/desk/<string:desk_ip>', methods=['GET'])
def get_desk(desk_id):
    desk = [desk for desk in desks if desk['ip'] == desk_ip]
    if len(desk) == 0:
        abort(404)
    return jsonify({'desk': desk[0]})
	
@app.route('/desk/<int:desk_beacon>', methods=['GET'])
def get_desk(desk_beacon):
    desk = [desk for desk in desks if desk['beacon'] == desk_beacon]
    if len(desk) == 0:
        abort(404)
    return jsonify({'desk': desk[0]})
	
@app.route('/desk', methods=['POST'])
def create_desk():
    if not request.json or not 'ip' in request.json:
        abort(400)
    desk = {
        'ip': request.json['ip'],
        'occupied': False,
        'beacon': request.json['beacon']
    }
    duplicate = [duplicate for duplicate in desks if duplicate['beacon'] == request.json['beacon']]
    if len(duplicate) != 0:
        abort(400)
    desks.append(desk)
    return jsonify({'desk': desk}), 201
	
@app.route('/desk/<int:desk_beacon>', methods=['PUT'])
def update_desk(desk_id):
    desk = [desk for desk in desks if desk['beacon'] == desk_beacon]
    if len(desk) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'ip' in request.json and type(request.json['ip']) != str:
        abort(400)
    if 'occupied' in request.json and type(request.json['occupied']) is not bool:
        abort(400)
    if 'beacon' in request.json and type(request.json['beacon']) is not int:
        abort(400)
    desk[0]['ip'] = request.json.get('ip', desk[0]['ip'])
    desk[0]['occupied'] = request.json.get('occupied', desk[0]['occupied'])
    desk[0]['beacon'] = request.json.get('beacon', desk[0]['beacon'])
    return jsonify({'desk': desk[0]})

@app.route('/test/<int:desk_beacon>', methods=['DELETE'])
def delete_desk(desk_beacon):
    desk = [desk for desk in desks if desk['beacon'] == desk_beacon]
    if len(desk) == 0:
        abort(404)
    desks.remove(desk[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
	
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
