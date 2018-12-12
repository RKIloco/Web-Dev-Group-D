from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class Item(db.Model):
    __tablename__ = 'Item'
    item_id = db.Column('item_id', db.Integer, unique=True, nullable=False,  primary_key=True)
    name = db.Column('name', db.String(80), unique=False, nullable=False)
    price = db.Column('price', db.Integer,  nullable=False)
    seller_name = db.Column('seller_name', db.String(80), nullable=False)
    link = db.Column('link', db.String(1000))

    def __init__(self,  name, price, seller_name, link):
        self.name = name
        self.seller_name = seller_name
        self.price = price
        self.link = link


# Event table template
class History(db.Model):
    __tablename__ = 'History'
    history_id = db.Column('history_id', db.Integer ,unique=True, nullable=False,  primary_key = True)
    name = db.Column('name', db.String(80), unique=False, nullable=False)
    price = db.Column('price', db.Integer,  nullable=False)
    buyer_name = db.Column('buyer_name', db.String(80), nullable=True)
    seller_name = db.Column('seller_name', db.String(80), nullable=True)
    link = db.Column('link', db.String(1000), nullable=True)

    def __init__(self, name, price, buyer_name, seller_name, link):
        self.name = name
        self.price = price
        self.buyer_name = buyer_name
        self.seller_name = seller_name
        self.link = link


# Featured Event table template
class Account(db.Model):
    __tablename_ = 'Account'
    account_id = db.Column('account_id', db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column('username', db.String(80), unique=True, nullable=False)
    password = db.Column('password', db.String(150),  nullable=False,)

    def __init__(self, username, password):

        self.username = username
        self.password = password


# User Events table template
class loggedin(db.Model):
    __tablename__ = 'loggedin'
    account_id = db.Column('account_id', db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column('username', db.String(80), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username


class DetailedUserSchema(ma.ModelSchema):
    class Meta:
        fields = ('item_id', 'name', 'price', 'seller_name', 'link')

class DetailedHistorySchema(ma.ModelSchema):
    class Meta:
        fields = ('history_id', 'name', 'price', 'buyer_name', 'seller_name', 'link')