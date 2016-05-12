from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db, Expenditure

from sqlalchemy.sql import and_

app = Flask(__name__)

app.secret_key = "CATS123"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage """

    # This is the homepage
    return render_template("homepage.html", user_session_info=session)


@app.route('/dashboard/<int:id>')
def dashboard(id):
    """ This is the user dashboard """

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:
        # This is the user object
        user = User.query.filter_by(id=id).first()

        # This is the expenditure object, which contains information about
        # expenditures specific to the user from the expenditure table in the
        # database
        expenditures = Expenditure.query.filter_by(expenditure_userid=id).all()

        # Renders the dashboard, which displays the following info
        return render_template("dashboard.html",
                                                name=user.name,
                                                password=user.password,
                                                email=user.email,
                                                expenditures=expenditures,
                                                id=id)


@app.route('/expenditure-form', methods=["GET", "POST"])
def expenditure_form():
    """ Add more expenditures on this expenditure form """

    # This is the homepage
    return render_template("expenditures-form.html")


@app.route('/add-expenditure-to-db', methods=["GET", "POST"])
def add_expenditure():
    """ Add new expenditure to the database """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Get values from the form
    category = request.form.get("category")
    price = request.form.get("price")
    date_of_expenditure = request.form.get("date")
    where_bought = request.form.get("wherebought")
    description = request.form.get("description")

    # Create a new expenditure object to insert into the expenditures table
    new_expenditure = Expenditure(category=category,
                                  price=price,
                                  date_of_expenditure=date_of_expenditure,
                                  where_bought=where_bought,
                                  description=description,
                                  expenditure_userid=id)

    # Insert the new expenditure into the expenditures table and commit the insert
    db.session.add(new_expenditure)
    db.session.commit()

    # Redirect to the dashboard
    return redirect(url_for('dashboard', id=id))


@app.route('/sign-up-form', methods=["GET", "POST"])
def sign_up_form():
    """ Sign up form """

    # Takes the user to the signup page
    return render_template("signup.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """ Sign up form consumption """

    # Gathering information from the sign up form
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # If the user does not exist, this will return None, and we will add them
    # to the database, otherwise we will flash an error message
    email_login_query = User.query.filter_by(email=email).first()

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

    # Should the user already exist in the database, this will
    # redirect them back to the homepage and flash a message that says
    # a user with that information already exists
    else:
        user_existence_check = User.query.filter(
                                                and_(
                                                    User.email == email,
                                                    User.password == password)).first()

        if user_existence_check:

            # Flash a message saying a user by this name already exists
            flash('A user by this name already exists')

            # Take the user back to the homepage
            return redirect(url_for("index"))


@app.route('/login', methods=["GET", "POST"])
def login():
    """ Directs the user to the login form """

    # Take the user to the login page
    return render_template("login.html")


@app.route('/login-form', methods=["GET", "POST"])
def login_form():
    """ Login form """

    # FIXME: login breaks if incorrect email but correct password
    # login works with incorrect password

    # Gather information from the login form
    email = request.form.get("email")
    password = request.form.get("password")

    # If either of these return None, the user will not be able to
    # successfully log in
    email_login_query = User.query.filter_by(email=email).first()
    password_login_query = User.query.filter_by(password=password).first()

    # Check if email_login_query is empty
    if email_login_query is None and password_login_query is None:

        # Flash an error message if the login information provided by the user
        # does not match any records
        flash('Error in logging in')

        # Take the user back to the homepage so they can try logging in again
        # or sign up if they haven't
        return redirect(url_for("index"))

    # If the user logs in with the incorrect email an error message will flash
    # and they will not be logged in
    elif email_login_query is None:

        flash('Error in logging in')

        return redirect(url_for("index"))

    # If the user logs in with the incorrect password an error message will flash
    # and they will not be logged in
    elif password_login_query is None:

        flash('Error in logging in')

        return redirect(url_for("index"))

    else:
        # Put the id into the session
        session['id'] = email_login_query.id

        # Take the user to the dashboard page, using their id
        return redirect(url_for('dashboard', id=session['id']))


@app.route('/logout', methods=["GET", "POST"])
def logout():

    # Remove the user id from the session if it exists
    session.pop('id', None)

    # Bring the user back to the homepage once they have been logged out
    return redirect(url_for('index'))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    spent_database = 'postgres:///spending'
    connect_to_db(app, spent_database)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
