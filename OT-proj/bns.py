import os

from flask import render_template, Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "itemsdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def verifyCC(cc):
    if len(cc) == 12 and cc[7] == cc[11] and ' ' not in cc:
        x = True
    else:
        x = False
    return x


class Item(db.Model):
    item_id = db.Column(db.Integer ,unique=True, nullable=False,  primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    seller_name = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return "<Product name: {}>".format(self.name) + "<Price: {}>".format(self.price) + "<Item id: {}>".format(self.item_id) + "<Seller name: {}>".format(self.seller_name) + "<Link: {}>".format(self.link)


class History(db.Model):
    history_id = db.Column(db.Integer ,unique=True, nullable=False,  primary_key = True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    buyer_name = db.Column(db.String(80), nullable=True)
    seller_name = db.Column(db.String(80), nullable=True)
    link = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return "<Product name: {}>".format(self.name) + "<Price: {}>".format(self.price) + "<History id: {}>".format(self.history_id) + "<Seller name: {}>".format(self.seller_name) ++ "<Buyer name: {}>".format(self.buyer_name) + "<Link: {}>".format(self.link)


class Account(db.Model):
    account_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150),  nullable=False,)

    def __repr__(self):
        return "<Username: {}>".format(self.username) + "<Password: {}>".format(self.password) + "<Acc_id: {}>".format(self.account_id)


class loggedin(db.Model):
    account_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Username: {}>".format(self.username) + "<Acc_id: {}>".format(self.account_id)


@app.route("/", methods=["GET", "POST"])
def  index():
    message = ""
    if request.form:
        try:
            if request.form.get("username") != "" and request.form.get("password") != "" and Account.query.filter_by(username=request.form.get("username")).first() == None  :
                password = bcrypt.generate_password_hash(request.form.get("password"))
                account = Account(username=request.form.get("username"), password=password)
                db.session.add(account)
                db.session.commit()
                message = "User created sucessfully"
            elif Account.query.filter_by(username=request.form.get("username")).first() != None:
                message = "User already exists"
            else:
                message = "Invalid input details"

        except Exception as e:

            return

    accounts = Account.query.all()
    return render_template("index.html", accounts=accounts,message = message)


@app.route("/signin", methods=["POST"])
def signin():
    if request.form :
        try:
                account = Account.query.filter_by(username=request.form.get("username")).first()
                if bcrypt.check_password_hash(account.password, request.form.get("password")):
                    loggedinaccount = loggedin(username=account.username)
                    db.session.add(loggedinaccount)
                    db.session.commit()
                    return redirect("/home")
                else:
                    return redirect("/")

        except Exception as e:

            return redirect ("/")

    accounts = Account.query.all()
    redirect("/")
    return render_template("index.html", accounts=accounts)


@app.route("/sell", methods=["GET", "POST"])
def sell():
    message = ""
    accountloggedin = loggedin.query.filter_by(account_id=1).first()

    if request.form:
        if request.form.get("name") != "" and request.form.get("price") != "":
            x = request.form.get("price")
            try:
                x = int(x)
                item = Item(name=request.form.get("name"), price=request.form.get("price"), link=request.form.get("link"), seller_name= accountloggedin.username)
                db.session.add(item)
                db.session.commit()
                message = "item successfully posted"
            except ValueError:
                message = "Invalid item details"

    return render_template("sell.html", message = message )


@app.route("/buy", methods=["GET", "POST"])
def buy():
    message = ""
    accountloggedin = loggedin.query.filter_by(account_id=1).first()
    if request.form:
        if request.form.get("bought_id"):

            to_be_bought = Item.query.filter_by(item_id=request.form.get("bought_id")).first()
            if to_be_bought:
                accountlogged = loggedin.query.filter_by(account_id="1").first()

                items = Item.query.filter(Item.seller_name != accountloggedin.username)
                if to_be_bought.seller_name == accountlogged.username:
                    return render_template("buy.html", items=items, message=message)

                bought_id = request.form.get("bought_id")
                return redirect("/buyitem/" + bought_id)

    items = Item.query.filter(Item.seller_name != accountloggedin.username)
    return render_template("buy.html", items=items, message=message)


@app.route("/buyitem/<int:bought_id>", methods=['GET',"POST"])
def hello_id(bought_id):
    bought_item = Item.query.filter_by(item_id= bought_id).first()
    accountloggedin = loggedin.query.filter_by(account_id=1).first()

    if request.form  and verifyCC(request.form.get("cc")) == True:
        toHistory = History(name=bought_item.name, price = bought_item.price, seller_name=bought_item.seller_name, link=bought_item.link, buyer_name=accountloggedin.username )
        db.session.add(toHistory)
        db.session.delete(bought_item)
        db.session.commit()
        return redirect("/buy")
    else:
        message = "Error buying item"

    return render_template("buyitem.html" , bought_item=bought_item, message = message)


@app.route("/home", methods=["GET"])
def home():
    accountloggedin = loggedin.query.all()
    return render_template("home.html", accountloggedin=accountloggedin)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    db.session.query(loggedin).delete()
    db.session.commit()

    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    accountloggedin = loggedin.query.filter_by(account_id=1).first()
    message = ""
    if request.form:
        item_id = request.form.get("item_id")
        item = Item.query.filter_by(item_id=item_id).first()
        if item:
            accountlogged = loggedin.query.filter_by(account_id="1").first()
            if item.seller_name != accountlogged.username:
                return redirect("/edit")
            else:
                if request.form.get("newname") != "" and request.form.get("newprice") != "":
                    item_id = request.form.get("item_id")

                    newname = request.form.get("newname")
                    item = Item.query.filter_by(item_id=item_id).first()
                    item.name = newname

                    newprice = request.form.get("newprice")
                    item = Item.query.filter_by(item_id=item_id).first()
                    item.price = newprice

                    newlink = request.form.get("newlink")
                    item = Item.query.filter_by(item_id=item_id).first()
                    item.link = newlink

                    db.session.commit()
                    message = "Item successfully updated"
                else:
                    message = "Failed to Edit item"

    items = Item.query.filter_by(seller_name=accountloggedin.username).all()
    return render_template("edit.html", items=items, message=message)


@app.route("/delete", methods=["POST"])
def delete():
    item_id = request.form.get("item_id")
    item = Item.query.filter_by(item_id=item_id).first()
    if item:
        accountlogged = loggedin.query.filter_by(account_id="1").first()
        if item.seller_name != accountlogged.username:
            return render_template("edit.html")
        else:
            db.session.delete(item)

            db.session.commit()
    return redirect("/edit")


@app.route("/history", methods=["GET"])
def history():
    accountloggedin = loggedin.query.first()
    history = History.query.filter((History.buyer_name == accountloggedin.username) | (History.seller_name == accountloggedin.username)).all()

    return render_template("history.html", history=history)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)