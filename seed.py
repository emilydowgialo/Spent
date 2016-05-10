""" Utility file to seed spending database in seed_data/ """

from sqlalchemy import func
from model import User, Expenditure

from model import connect_to_db, db
from server import app
# import datetime


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
        email = user_data[1]
        password = user_data[2]
        username = user_data[3]

        user = User(id=id,
                    email=email,
                    password=password,
                    username=username)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

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
        category = expenditure_data[1]
        price = expenditure_data[2]
        date_of_expenditure = expenditure_data[3]
        expenditure_userid = expenditure_data[4]
        where_bought = expenditure_data[5]
        description = expenditure_data[6]

        # convert date_of_expenditure from string to datetime format
        # if date_of_expenditure:
        #     date_of_expenditure = datetime.datetime.strptime(date_of_expenditure, '%d-%b-%Y')
        # else:
        #     date_of_expenditure = None

        expenditure = Expenditure(id=id,
                                  category=category,
                                  price=price,
                                  date_of_expenditure=date_of_expenditure,
                                  expenditure_userid=expenditure_userid,
                                  where_bought=where_bought,
                                  description=description)

        db.session.add(expenditure)

    db.session.commit()


def set_val_user_id():
    """ Set value for the next user_id after seeding database """

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_expenditures()
