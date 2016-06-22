from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    BigInteger, Boolean, Date, Time, Float, ForeignKey, DateTime, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .meta import Base

engine = create_engine('sqlite:///bookingsystem.sqlite')
Session = sessionmaker()
Base = declarative_base(bind=engine)

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('ix_names', MyModel.name, unique=True, mysql_length=255)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card = Column(Text)
    name = Column(Text, nullable=False)
    sex = Column(Boolean, nullable=False)
    birth = Column(Date, nullable=False)
    document = Column(Text, nullable=False, unique=True)
    phone = Column(Text)

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

class Airport(Base):
    __tablename__ = 'airports'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(Text)
    address = Column(Text)

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    number = Column(Text, nullable=False)
    airport_id = Column(Integer,  ForeignKey("airports.id"), nullable=False)
    toairport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    date_dep = Column(Date, nullable=False)
    time_dep = Column(Time)
    date_arr = Column(Date, nullable=False)
    time_arr = Column(Time)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

class Seat(Base):
    __tablename__ = 'seats'
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Float)
    tax = Column(Float)
    baggage = Column(Float)
    count = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)	
    user = Column(Integer, ForeignKey("users.id"), nullable=False)

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    code = Column(Text, nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    totalprice = Column(Float)



