""" Utility file to seed spending database in seed_data/ """

from sqlalchemy import func
from model import User, Expenditure, Budget, Category

from model import connect_to_db, db
from server import app

import os


def load_users():
    """ Load users from users.csv into database """

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read users.csv file and insert data into the session
    for row in open("seed_data/users.csv"):
        row = row.rstrip()
        user_data = row.split("|")
        id = user_data[0]
        name = user_data[1]
        email = user_data[2]
        password = user_data[3]

        user = User(id=id,
                    name=name,
                    email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_categories():
    """ Load categories from categories.csv into database """

    print "Categories"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate categories
    Category.query.delete()

    # Read categories.csv file and insert data into the session
    for row in open("seed_data/categories.csv"):
        row = row.rstrip()
        categories_data = row.split("|")
        id = categories_data[0]
        category = categories_data[1]

        category_model = Category(id=id,
                                  category=category)

        # We need to add to the session or it won't ever be stored
        db.session.add(category_model)

    db.session.commit()


def load_budget():
    """ Load budget from budget.csv into database """

    print "Budget"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Budget.query.delete()

    # Read users.csv file and insert data into the session
    for row in open("seed_data/budget.csv"):
        row = row.rstrip()
        budget_data = row.split("|")
        id = budget_data[0]
        budget = budget_data[1]
        category_id = budget_data[2]
        budget_userid = budget_data[3]
        budget_start_date = budget_data[4]
        budget_end_date = budget_data[5]

        budget = Budget(id=id,
                        budget=budget,
                        category_id=category_id,
                        budget_userid=budget_userid,
                        budget_start_date=budget_start_date,
                        budget_end_date=budget_end_date)

        # We need to add to the session or it won't ever be stored
        db.session.add(budget)

    # Once we're done, we should commit our work
    db.session.commit()


def load_expenditures():
    """ Load expenditures from expenditures.csv into database """

    print "Expenditures"
    Expenditure.query.delete()

    for row in open("seed_data/expenditures.csv"):
        row = row.rstrip()
        expenditure_data = row.split("|")
        id = expenditure_data[0]
        category_id = expenditure_data[1]
        price = expenditure_data[2]
        date_of_expenditure = expenditure_data[3]
        expenditure_userid = expenditure_data[4]
        where_bought = expenditure_data[5]
        description = expenditure_data[6]
        tracking_num = expenditure_data[7]
        tracking_num_carrier = expenditure_data[8]

        expenditure = Expenditure(id=id,
                                  category_id=category_id,
                                  price=price,
                                  date_of_expenditure=date_of_expenditure,
                                  expenditure_userid=expenditure_userid,
                                  where_bought=where_bought,
                                  description=description,
                                  tracking_num=tracking_num,
                                  tracking_num_carrier=tracking_num_carrier)

        db.session.add(expenditure)

    db.session.commit()


def set_val_user_id():
    """ Set value for the next user id after seeding database """

    # Get the Max user id in the database
    result = db.session.query(func.max(User.id)).one()

    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    # Note to self: the 'users_id_seq' variable is based on the Users table
    query = "SELECT setval('users_id_seq', :new_id)"

    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_expenditure_id():
    """ Set value for the next expenditure id after seeding database """

    # Get the Max expenditure id in the database
    result = db.session.query(func.max(Expenditure.id)).one()

    max_id = int(result[0])

    # Set the value for the next expenditure id to be max_id + 1
    query = "SELECT setval('expenditures_id_seq', :new_id)"

    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_budget_id():
    """ Set value for the next budget id after seeding database """

    # Get the Max user id in the database
    result = db.session.query(func.max(Budget.id)).one()

    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('budget_id_seq', :new_id)"

    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_category_id():
    """ Set value for the next category id after seeding database """

    # Get the Max user id in the database
    result = db.session.query(func.max(Category.id)).one()

    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('categories_id_seq', :new_id)"

    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    spent_database = os.getenv('POSTGRES_DB_URL', 'postgres:///spending')
    connect_to_db(app, spent_database)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_categories()
    load_expenditures()
    load_budget()
    set_val_user_id()
    set_val_category_id()
    set_val_expenditure_id()
    set_val_budget_id()
