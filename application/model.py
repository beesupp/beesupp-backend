from database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from datetime import datetime

class User(Base):
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)

    name = Column(Text)
    surname = Column(Text)
    created_date = Column(DateTime, default=datetime.utcnow)
    vehicle = relationship("Vehicle", back_populates="user")
    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()

class Vehicle(Base): # it can be AMG, C180, C200 etc.
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.
    __tablename__ = "vehicle"
    # We always need an id
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="vehicle")
    item = relationship("Item", back_populates="vehicle")
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()

class Item(Base):
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.
    __tablename__ = "item"
    # We always need an id
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"))
    vehicle = relationship("Vehicle", back_populates="item")
    name = Column(Text)
    created_date = Column(DateTime, default=datetime.utcnow)
    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()