import os

from flask import render_template, Flask, request, redirect, jsonify, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_reverse_proxy import FlaskReverseProxied

from config import Configuration
from models import db, ma, Item, History, Account, loggedin, DetailedUserSchema

from models import *
import click
from flask.cli import FlaskGroup

proxy = FlaskReverseProxied()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Configuration.SQLALCHEMY_DATABASE_URI
proxy.init_app(app)
db.init_app(app)
ma.init_app(app)

CORS(app)

bcrypt = Bcrypt(app)


@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Management script for the flask application."""


@cli.command('init_db')
def init_db():
    # Initialize tables
    db.create_all()
    db.session.commit()
    print("Tables Created")


@cli.command('drop_db')
def delete_db():
    with app.app_context():
        db.drop_all()
    print("Tables dropped")


def verifyCC(cc):
    if len(cc) == 12 and cc[7] == cc[11] and ' ' not in cc:
        x = True
    else:
        x = False
    return x







@app.route("/", methods=["POST"])
def  index():
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    try:
        if username != "" and password != "" and Account.query.filter_by(username=username).first() == None  :
            password = bcrypt.generate_password_hash(password)
            account = Account(username=username, password=password)
            db.session.add(account)
            db.session.commit()
            message = "Account Created"
            return message
        elif Account.query.filter_by(username=username).first() != None:
            message = "User already exists"
            return message
        else:
            message = "Invalid input details"
            return message
    except Exception as e:
            return
    accounts = Account.query.all()
    return message


@app.route("/signin", methods=["POST"])
def signin():
    logged = ""
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    account = Account.query.filter_by(username=username).first()
    if account == None:
        logged = "0"
        return logged
    else:
        if bcrypt.check_password_hash(account.password, password):
            openaccount = loggedin.query.first()
            if openaccount != None:
                db.session.delete(openaccount)
                db.session.commit() 
            loggedinaccount = loggedin(username=account.username)
            db.session.add(loggedinaccount)
            db.session.commit()
            logged = account.password
            return logged
        else:
            logged = "0"
            return logged
    return logged

@app.route("/logout", methods=["POST"])
def logout():
    payload = request.get_json()
    logged = payload.get('logged')
    accountlogged = loggedin.query.first()
    db.session.delete(accountlogged)
    db.session.commit()
    return logged


@app.route("/sell", methods=["POST"])
def sell():
    payload = request.get_json()
    name = payload.get('name')
    price = payload.get('price')
    image = payload.get('image')
    message = ""
    accountloggedin = loggedin.query.first()
    if name != "" and price != "":
        item = Item(name=name, price=price, link=image, seller_name= accountloggedin.username)
        db.session.add(item)
        db.session.commit()
        message = "Item successfully posted"
        return message
    else:
        message = "Invalid item details"
        return message
    return message


@app.route("/items", methods=["GET"])
def items_to_sell():
    account = loggedin.query.first()
    items = Item.query.filter(Item.seller_name != account.username).all()
    schema = DetailedUserSchema(many=True)
    response = schema.jsonify(items)
    return response

@app.route("/youritems", methods=["GET"])
def kimi_no_item_wa():
    account = loggedin.query.first()
    items = Item.query.filter_by(seller_name=account.username).all()
    schema = DetailedUserSchema(many=True)
    response = schema.jsonify(items)
    return response


@app.route("/boughtitem", methods=["POST"])
def item_to_be_bought():
    payload = request.get_json()
    bought_item_id = payload.get('id_item')
    bought_item = Item.query.filter_by(item_id=bought_item_id).first()
    schema = DetailedUserSchema()
    response = schema.jsonify(bought_item)
    return response

@app.route("/buyid", methods=["POST"])
def id_of_item():
    payload = request.get_json()
    id_of_item = payload.get('bought_id')
    accountid = loggedin.query.first()
    item = Item.query.filter_by(item_id=id_of_item).first()
    message = ""
    if item.seller_name == accountid.username or item == None:
        message = "Invalid ID"
        return message
    else:
        message = ""
        return message
    return message


@app.route("/buy", methods=["POST"])
def buy():
    message = ""
    payload = request.get_json()
    bought_id = payload.get('bought_id')
    cc = payload.get('cc')
    bought_item = Item.query.filter_by(item_id= bought_id).first()
    accountloggedin = loggedin.query.first()
    if bought_item.seller_name != accountloggedin.username or bought_id == None:
        message = "Invalid ID"
        return message
    else:
        if verifyCC(cc) == True:
            toHistory = History(name=bought_item.name, price = bought_item.price, seller_name=bought_item.seller_name, link=bought_item.link, buyer_name=accountloggedin.username )
            db.session.add(toHistory)
            db.session.delete(bought_item)
            db.session.commit()
            message = ""
            return message
        else:
            message = "Error buying item"
            return message
    return message


@app.route("/edit", methods=["POST"])
def edit():
    payload = request.get_json()
    newname = payload.get('name')
    newprice = payload.get('price')
    newlink = payload.get('image')
    item_id = payload.get('bought_id')
    message = ""
    item = Item.query.filter_by(item_id=item_id).first()
    if newname == "":
        item.name = item.name
    else:
        item.name = newname

    if newprice == "":
        item.price = item.price
    else:
        item.price = newprice

    if newlink == "":
        item.link = item.link
    else:
        item.link = newlink
        
    db.session.commit()
    message = "Item successfully updated"
    return message


@app.route("/delete", methods=["POST"])
def delete():
    payload = request.get_json()
    item_id = payload.get('bought_id')
    message = ""
    item = Item.query.filter_by(item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    message = "Item successfully deleted"
    return message


@app.route("/history", methods=["GET"])
def history():
    accountloggedin = loggedin.query.first()
    history = History.query.filter((History.buyer_name == accountloggedin.username) | (History.seller_name == accountloggedin.username)).all()
    schema = DetailedHistorySchema(many=True)
    response = schema.jsonify(history)
    return response


if __name__ == '__main__':
    cli()