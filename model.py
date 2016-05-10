
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ This is the user of the web app """

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64))


class Expenditure(db.Model):
    """ This contains expenditures """

    __tablename__ = "expenditures"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(64))
    price = db.Column(db.Numeric(15, 2))
    # Tell users to enter in 2014-03-12. On backend, datetime.datetime.strptime('2014-03-12', '%Y-%m-%d')
    # bootstrap datepicker
    date_of_expenditure = db.Column(db.DateTime)
    # Will know the user id based on who is logged in to the session
    expenditure_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    where_bought = db.Column(db.String(100), nullable=True)
    description = db.Column(db.UnicodeText, nullable=True)
    # tracking_num = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", backref=db.backref('expenditures'))


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """ Connect the database to our Flask app. """

    # Configure to use the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///spending'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
