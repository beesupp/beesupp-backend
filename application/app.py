from flask import Flask, request
import json
from database import *

app = Flask(__name__)

# CRUD - READ requests
@app.route('/get_all_users')
def get_all_users():
    all_users_dict = get_all_users_from_db()
    all_users_resp = {}
    all_users_resp['users'] = all_users_dict
    all_users_resp['code'] = 200
    return json.dumps(all_users_resp)

@app.route('/get_all_vehicles')
def get_all_vehicles():
    all_vehicles_dict = get_all_vehicles_from_db()
    all_vehicles_resp = {}
    all_vehicles_resp['vehicles'] = all_vehicles_dict
    all_vehicles_resp['code'] = 200
    return json.dumps(all_vehicles_resp)

@app.route('/get_all_vehicle_items')
def get_all_vehicle_items():
    all_vehicle_items_dict = get_all_vehicle_items_from_db()
    all_vehicle_items_resp = {}
    all_vehicle_items_resp['items'] = all_vehicle_items_dict
    all_vehicle_items_resp['code'] = 200
    return json.dumps(all_vehicle_items_resp)

# CRUD - CREATE requests
@app.route('/create_new_user', methods=['POST'])
def create_new_user():
    new_user_name = request.json["user_name"]
    create_user(new_user_name)
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)

@app.route('/create_new_vehicle', methods=['POST'])
def create_new_vehicle():
    new_vehicle_name = request.json["vehicle_name"]
    create_vehicle(user_name="BeeSuppDefUser", user_vehicle_name=new_vehicle_name)
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)

@app.route('/create_new_vehicle_item', methods=['POST'])
def create_new_vehicle_item():
    new_vehicle_item = request.json["item_name"]
    create_vehicle_item(item_name=new_vehicle_item, item_vehicle_name="BeeSuppDefVehicle", item_user_name="BeeSuppDefUser")
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5888)