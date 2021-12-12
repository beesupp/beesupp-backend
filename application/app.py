from flask import Flask, request
import json
from database import *
import payment

import logging
import coloredlogs

loggerTest = logging.getLogger("bee_TEST")
loggerTest.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=loggerTest, milliseconds=True, fmt='[%(levelname)s]-> %(message)s')

app = Flask(__name__)

# CRUD - READ requests
@app.route('/get_all_users')
def get_all_users():
    all_users_dict = get_all_users_from_db()
    all_users_resp = {}
    all_users_resp['users'] = all_users_dict
    all_users_resp['code'] = 200
    return json.dumps(all_users_resp)

@app.route('/set_current_active_user', methods=['POST'])
def set_current_active_user():
    new_vehicle_name = request.json["vehicle_name"]
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)

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

@app.route('/get_all_user_vehicle_items', methods=['POST'])
def get_all_user_vehicle_items():
    selected_user_name = request.json["user_name"]
    all_vehicle_items_dict = get_all_user_vehicle_items_from_db(selected_user_name)
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

''' TODO  
@app.route('/create_new_vehicle_item', methods=['POST'])
def create_new_vehicle_item():
    new_item_category = request.json["new_item_category"]
    new_item_name = request.json["new_item_name"]
    new_item_description = request.json["new_item_description"]
    new_item_price = request.json["item_name"]
    new_item_category = request.json["item_name"]
    new_vehicle_item = request.json["item_name"]
    create_vehicle_item(new_item_category, new_item_name, new_item_description, new_item_price, new_item_image, "BeeSuppDefVehicle", "BeeSuppDefUser")
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)
'''

@app.route('/buy_vehicle_item', methods=['POST'])
def buy_vehicle_item():
    buy_item_name = request.json["buy_item_name"]
    loggerTest.warning("satin alinan: " + buy_item_name)
    pay_res = payment.buy(buy_item_name)
    resp = {}
    if pay_res:
        resp['msg'] = "Success"
        resp['code'] = 200
        change_item_owner(buy_item_name, "Ertan")
    else:
        resp['msg'] = "Failure"
        resp['code'] = 1001
    return json.dumps(resp)

@app.route('/logged_user', methods=['POST'])
def logged_user():
    logged_user_id = request.json["user_id"]
    if logged_user_id == 0:
        loggerTest.warning("log user alinan: Kivanc")
    else:
        loggerTest.warning("log user alinan: Ertan")
    resp = {}
    resp['msg'] = "Success"
    resp['code'] = 200
    return json.dumps(resp)

if __name__ == "__main__":
    init_database_tables()
    app.run(debug=True, host='0.0.0.0', port=5888)