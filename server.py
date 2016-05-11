from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db

from sqlalchemy.sql import and_

app = Flask(__name__)

app.secret_key = "CATS123"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage """

    return render_template("homepage.html", user_session_info=session)


# @app.route('/dashboard/<int:id>')
# def dashboard():
#     """ This is the user dashboard """

#     # if the user is logged into the session, check the user's id
#     # and gather information about the user based on this
#     if id in session:
#         user = User.query.filter_by(id=id).first()

#     return render_template("dashboard.html",
#                             email=user.email,
#                             password=user.password,
#                             username=user.username)

@app.route('/sign-up-form', methods=["GET", "POST"])
def sign_up_form():
    """ Sign up form """

    return render_template("signup.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """ Sign up form consumption """
    # FIXME

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    email_login_query = User.query.filter_by(email=email).first()
    print
    print
    print
    print email_login_query
    print
    print
    print

    # Check if user already exists
    if email_login_query is None:

        # If the user does not exist in the database, we add the user
        new_user = User()

        # Set the new user's name, email, and password
        new_user.name = name
        new_user.email = email
        new_user.password = password

        # Add the new user to the session - this is a database insertion
        db.session.add(new_user)
        db.session.commit()

        # Flash a message confirming the user has successfully signed up
        flash('You have successfully signed up')

        return redirect(url_for('index'))

    # If the user already exists in the database
    else:
        user_existence_check = User.query.filter(
                                                and_(
                                                    User.email == email,
                                                    User.password == password)).first()

        # Should the user already exist in the database, this will
        # redirect them back to the homepage and flash a message that says
        # a user with that information already exists
        if user_existence_check:

            # Flash a message saying a user by this name already exists
            flash('A user by this name already exists')

            return redirect(url_for("index"))


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     email = request.form.get("email")
#     password = request.form.get("password")

#     email_login_query = User.query.filter_by(email=email).first()

#     # Check if email_login_query is empty
#     if email_login_query:


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
