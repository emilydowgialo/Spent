
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ This is the user of the web app """

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64))


class Budget(db.Model):
    """ This is the user's budget """

    __tablename__ = "budget"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # the data type of the budget should match the data type of the price
    budget = db.Column(db.Numeric(15, 2))
    category = db.Column(db.String(64), nullable=True)
    budget_userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref=db.backref('budget'))


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

    spent_database = 'postgres:///spending'

    connect_to_db(app, spent_database)
    print "Connected to DB."


def connect_to_db(app, spent_database):
    """ Connect the database to our Flask app. """

    # spent_database = 'postgres:///spending'

    # Configure to use the database
    app.config['SQLALCHEMY_DATABASE_URI'] = spent_database
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""

    fakeuser = User(name="Mu", email="mu@mu.com", password="mu")
    fakebudget = Budget(budget=1000, category="Food", budget_userid=fakeuser.id)
    fakeexpenditure = Expenditure(category="Travel", price=500, date_of_expenditure="2016-05-07", expenditure_userid=fakeuser.id, where_bought="train station", description="Amtrak ticket")

    db.session.add_all([fakeuser, fakebudget, fakeexpenditure])
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    spent_database = 'postgres:///spending'

    connect_to_db(app, spent_database)
    print "Connected to DB."
