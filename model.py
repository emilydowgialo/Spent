
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()


class User(db.Model):
    """ This is the user of the web app """

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))


class Category(db.Model):
    """ This is the category table """

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(64))


class Budget(db.Model):
    """ This is the user's budget """

    __tablename__ = "budget"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # the data type of the budget should match the data type of the price
    budget = db.Column(db.Numeric(15, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    budget_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    budget_start_date = db.Column(db.DateTime)
    budget_end_date = db.Column(db.DateTime)

    user = db.relationship("User", backref=db.backref('budget'))

    category = db.relationship("Category", backref=db.backref('budget'))

    def __repr__(self):
        """ Provide useful info """

        return "<Budget id=%s budget=%s budget_userid=%s category=%s budget_start_date=%s budget_end_date=%s>" % (
            self.id, self.budget, self.budget_userid, self.category, self.budget_start_date, self.budget_end_date)


class Expenditure(db.Model):
    """ This contains expenditures """

    __tablename__ = "expenditures"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price = db.Column(db.Numeric(15, 2))
    date_of_expenditure = db.Column(db.DateTime)
    expenditure_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    where_bought = db.Column(db.String(100))
    description = db.Column(db.UnicodeText)
    tracking_num = db.Column(db.String, nullable=True)
    tracking_num_carrier = db.Column(db.String(100), nullable=True)

    user = db.relationship("User", backref=db.backref('expenditures'))

    category = db.relationship("Category", backref=db.backref('expenditures'))


def connect_to_db(app, spent_database):
    """ Connect the database to our Flask app. """

    # Configure to use the database
    app.config['SQLALCHEMY_DATABASE_URI'] = spent_database
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""

    fakeuser = User(name="Mu", email="mu@mu.com", password="mu")
    fakebudget = Budget(budget=1000, category_id=3, budget_start_date="2016-05-07", budget_end_date="2016-06-15")
    fakecat = Category(category="Food", id=3)
    fakecat2 = Category(category="Travel", id=2)
    fakeexpenditure = Expenditure(category_id=2, price=500,
                                  date_of_expenditure="2016-05-07",
                                  expenditure_userid=fakeuser.id,
                                  where_bought="train station",
                                  description="Amtrak ticket")

    db.session.add_all([fakeuser, fakebudget, fakeexpenditure, fakecat, fakecat2])
    db.session.commit()

    # Add the budget_userid to the database, otherwise budget_userid is None
    # because the budget is not associated with a user
    fakebudget.budget_userid = fakeuser.id
    db.session.add(fakebudget)
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    spent_database = os.getenv('POSTGRES_DB_URL', 'postgres:///spending')

    connect_to_db(app, spent_database)
    print "Connected to DB."
