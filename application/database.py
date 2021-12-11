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