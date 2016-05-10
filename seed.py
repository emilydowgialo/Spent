"""Utility file to seed spending database in seed_data/"""

from sqlalchemy import func
from model import User, Expenditure

from model import connect_to_db, db
from server import app
import datetime


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
                    password=password,
                    username=username)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_expenditures():
    """ Load movies from expenditures.csv into database """

    print "Expenditures"
    Movie.query.delete()

    for row in open("seed_data/expenditures.csv"):
        row = row.rstrip()
        expenditure_data = row.split("|")
        category = expenditure_data[0]
        title = movies_data[1]
        released_at = movies_data[2]
        imdb_url = movies_data[4]


        # this list holds the title and the date
        title = title[:-6].rstrip()

        # convert released_at from string to datetime format
        if released_at:
            released_at = datetime.datetime.strptime(released_at, '%d-%b-%Y')
        else:
            released_at = None

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()
