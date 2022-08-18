from flask import Flask, request
from flask_cors import CORS, cross_origin


import json


import threading

from database import Database
from sensor import Sensor


app = Flask(__name__)
app.debug = True
CORS(app,  resources={r"/api/*": {"origins": "*"}})

broker = Database()


@app.route('/play')
def play():
    try:
        # TODO: pegar porta serial de acordo com o OS
        sensor = Sensor("/dev/ttyUSB0", broker)
        ret = sensor.open()
        return json.dumps({'message': ret}), 200, {'ContentType': 'application/json'}

    except Exception as e:
        # return json.dumps({'message': "Simulando os dados"}), 200, {'ContentType': 'application/json'}
        # return json.dumps({'message': 'Serial port error({0}): {1}\n\n'.format(e.errno, e.strerror)}), 400, {'ContentType': 'application/json'}
        return json.dumps({'message': str(e)}), 400, {'ContentType': 'application/json'}


@app.route('/data', methods=['GET'])
def get_data():
    data = broker.get_all_data('raw_data')
    return json.dumps(data,  default=str)


@app.route('/')
def index():
    return {"hello": "world"}


'''USER APIS'''


@app.route('/user/', methods=['GET'])
@cross_origin()
def get_users():
    try:
        data = broker.get_users()  # get_all_data('users')
        return json.dumps(data,  default=str)
    except Exception as e:
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}


@app.route('/user/add', methods=['POST'])
@cross_origin()
def add_user():
    try:
        broker.save_user(request.get_json()['user_name'])
        return json.dumps({'user': "user in added successfully"}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}


@app.route('/user/delete/<id>', methods=['DELETE'])
@cross_origin()
def delete_user(id):
    try:
        print(id)
        broker.delete_user(id)
        return json.dumps({'user': "User deleted"}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}


@app.route('/user/edit/<id>', methods=['GET'])
@cross_origin()
def edit_user(id):
    try:
        data = broker.get_user_by_id(id)
        return json.dumps(data,  default=str), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}


@app.route('/user/update/<id>', methods=['PUT'])
@cross_origin()
def update_user(id):
    try:
        broker.update_user(id, request.get_json()['user_name'])
        return json.dumps({'user': "user updated successfully"}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 400, {'ContentType': 'application/json'}


if __name__ == '__main__':
    # app.run(threaded=True)
    app.run(host='127.0.0.1', port=5000,    threaded=True)
