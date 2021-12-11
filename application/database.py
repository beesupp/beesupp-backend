import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

from model import User, MercedesVehicle, MercedesVehicleItem
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
        selected_user_vehicles = User.query.join(MercedesVehicle).filter(
            User.name == user_name).filter(MercedesVehicle.name == user_vehicle_name).all()
        # if selected user does not have specified vehicle, insert it
        if len(selected_user_vehicles) == 0:
            selected_user_entry = User.query.get(selected_user.id)
            new_vehicle = MercedesVehicle(user_vehicle_name)
            selected_user_entry.vehicle.append(new_vehicle)
            db_session.commit()

def create_vehicle_item(item_name, item_vehicle_name, item_user_name):
    selected_vehicle = MercedesVehicle.query.join(User).filter(
        User.name == item_user_name).filter(MercedesVehicle.name == item_vehicle_name).first()
    if selected_vehicle is not None:
        selected_vehicle_items = User.query.join(MercedesVehicle).join(MercedesVehicleItem).filter(User.name == item_user_name).filter(
            MercedesVehicle.name == item_vehicle_name).filter(MercedesVehicleItem.name == item_name).all()
        if len(selected_vehicle_items) == 0:
            new_item = MercedesVehicleItem(item_name)
            selected_vehicle.vehicle_item.append(new_item)
            db_session.commit()

def get_all_users():
    all_users_arr = []
    all_users = db_session.query(User)
    for user in all_users:
        each_user = {}
        each_user['name'] = user.name
        all_users_arr.append(each_user)
        print("User: " + user.name)
    return all_users_arr

def get_all_vehicles():
    all_vehicles_arr = []
    all_vehicles = db_session.query(MercedesVehicle)
    for vehicle in all_vehicles:
        each_vehicle = {}
        each_vehicle['name'] = vehicle.name
        all_vehicles_arr.append(each_vehicle)
        print("Vehicle listed: " + vehicle.name)
    return all_vehicles_arr

def get_all_vehicle_items():
    all_items_arr = []
    all_mercedes_vehicle_items = db_session.query(MercedesVehicleItem)
    for item in all_mercedes_vehicle_items:
        each_item = {}
        each_item['name'] = item.name
        all_items_arr.append(each_item)
        print("Item listed: " + item.name)
    return all_items_arr

def inject_mock_data():
    create_user("BeeSuppDefUser")
    create_vehicle("BeeSuppDefVehicle")