import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import coloredlogs

loggerTest = logging.getLogger("bee_TEST")
loggerTest.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=loggerTest, milliseconds=True, fmt='[%(levelname)s]-> %(message)s')

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'database'
port = '5432'

engine = create_engine('postgres://%s:%s@%s:%s/%s' %
                       (user, pwd, host, port, db))

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from model import User, Vehicle, Item
# import all modules here that might define Models so that
# they will be registered properly on the metadata.  Otherwise
# you will have to import them first before calling init_database_tables()

def init_database_tables():
    # If table don't exist, Create.
    if not engine.dialect.has_table(engine, "user"):
        Base.metadata.create_all(bind=engine)
        # after table creation, insert def/mock data
        inject_mock_data()

def create_user(user_name):
    contains = bool(User.query.filter_by(name=user_name).first())
    if not contains:  # if not contains, add it
        new_user = User(name=user_name)
        db_session.add(new_user)
        db_session.commit()

def create_vehicle(user_name, user_vehicle_name):
    selected_user = User.query.filter_by(name=user_name).first()
    if selected_user is not None:
        selected_user_vehicles = User.query.join(Vehicle).filter(
            User.name == user_name).filter(Vehicle.name == user_vehicle_name).all()
        # if selected user does not have specified vehicle, insert it
        if len(selected_user_vehicles) == 0:
            selected_user_entry = User.query.get(selected_user.id)
            new_vehicle = Vehicle(user_vehicle_name)
            selected_user_entry.vehicle.append(new_vehicle)
            db_session.commit()

def create_vehicle_item(item_category, item_name, item_description, item_price, item_image, item_vehicle_name, item_user_name):
    selected_vehicle = Vehicle.query.join(User).filter(
        User.name == item_user_name).filter(Vehicle.name == item_vehicle_name).first()
    if selected_vehicle is not None:
        selected_vehicle_items = User.query.join(Vehicle).join(Item).filter(User.name == item_user_name).filter(
            Vehicle.name == item_vehicle_name).filter(Item.name == item_name).all()
        if len(selected_vehicle_items) == 0:
            new_item = Item(item_category, item_name, item_description, item_price, item_image)
            selected_vehicle.item.append(new_item)
            db_session.commit()

def get_all_users_from_db():
    all_users_arr = []
    all_users = db_session.query(User)
    for user in all_users:
        each_user = {}
        each_user['id'] = user.id
        each_user['name'] = user.name
        if user.is_current_user:
            each_user['is_active'] = "True"
        else:
            each_user['is_active'] = "False"
        all_users_arr.append(each_user)
        print("User: " + user.name)
    return all_users_arr

def get_all_vehicles_from_db():
    all_vehicles_arr = []
    all_vehicles = db_session.query(Vehicle)
    for vehicle in all_vehicles:
        each_vehicle = {}
        each_vehicle['name'] = vehicle.name
        all_vehicles_arr.append(each_vehicle)
        print("Vehicle listed: " + vehicle.name)
    return all_vehicles_arr

def get_all_vehicle_items_from_db():
    all_items_arr = []
    all_mercedes_vehicle_items = db_session.query(Item)
    for item in all_mercedes_vehicle_items:
        each_item = {}
        each_item['id'] = item.id
        each_item['category'] = item.category
        each_item['title'] = item.name
        each_item['description'] = item.description
        each_item['price'] = item.price
        each_item['image'] = item.image
        each_item['owner_name'] = item.owner
        all_items_arr.append(each_item)
        print("Item listed: " + item.name)
    return all_items_arr

def get_all_user_vehicle_items_from_db(specific_username):
    all_items_arr = []
    all_mercedes_vehicle_items = db_session.query(Item).filter(Item.owner == specific_username).all()
    for item in all_mercedes_vehicle_items:
        each_item = {}
        each_item['id'] = item.id
        each_item['category'] = item.category
        each_item['title'] = item.name
        each_item['description'] = item.description
        each_item['price'] = item.price
        each_item['image'] = item.image
        each_item['owner_name'] = item.owner
        all_items_arr.append(each_item)
        print("Item listed: " + item.name)
    return all_items_arr

def set_current_user(user_id):
    curr_active_user = db_session.query(User).filter(User.is_current_user == True).first()
    if curr_active_user is not None:
        curr_active_user.is_current_user = False
    selected_user = User.query.filter_by(id=user_id).first()
    if selected_user is not None and selected_user.is_current_user == False:
        selected_user.is_current_user = False
        db_session.commit()

def get_current_user():
    curr_active_user = db_session.query(User).filter(User.is_current_user == True)
    if curr_active_user is not None:
        return curr_active_user.id

def change_item_owner(item_name, new_owner_name):
    selected_item = db_session.query(Item).filter(Item.name == item_name).first()
    if selected_item is not None:
        selected_item.owner = new_owner_name
        db_session.commit()

def inject_mock_data():
    create_user("BeeSuppDefUser")
    create_user("Ertan")
    create_user("Kivanc")
    create_vehicle("Ertan", "amg")
    create_vehicle("Ertan", "c180")
    create_vehicle("Ertan", "s2000")
    create_vehicle("Kivanc", "amg")
    create_vehicle("Kivanc", "c180")
    create_vehicle("Kivanc", "s2000")
    create_vehicle("BeeSuppDefUser", "BeeSuppDefVehicle")
    create_vehicle("BeeSuppDefUser", "amg")
    create_vehicle("BeeSuppDefUser", "c180")
    create_vehicle("BeeSuppDefUser", "s2000")
    create_vehicle_item("Themes", "Default", "very cool", "1000", "default_inside.png", "amg", "BeeSuppDefUser")
    create_vehicle_item("Themes", "Sport", "very cool", "1000", "sport_inside.png", "c180", "BeeSuppDefUser")
    create_vehicle_item("NFTs", "Star", "very cool", "10", "star_inside.png", "s2000", "BeeSuppDefUser")