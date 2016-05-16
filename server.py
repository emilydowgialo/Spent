from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, url_for, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db, Expenditure, Budget

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

        # This is the user's budget
        budget = Budget.query.filter_by(id=id).first()
        new_budget = budget.budget
        budget_category = budget.category

        print
        print "this is budget"
        print budget
        print
        print "category"
        print budget_category
        print
        print

        # This is the expenditure object, which contains information about
        # expenditures specific to the user from the expenditure table in the
        # database
        expenditures = Expenditure.query.filter_by(expenditure_userid=id).all()

        ########################################################################
        # CALCULATE TOTALS FOR EACH EXPENDITURE CATEGORY
        ########################################################################

        # Food expenditure total
        expenditures_food = Expenditure.query.filter_by(category="Food", expenditure_userid=id).all()

        # This is total amount spent - it will be increased with every purchase
        total_spent = 0

        # Loop through each item in the food category, add up the prices
        i = 0
        total_food_price = 0

        for food_expenditure in expenditures_food:
            food_expenditure = expenditures_food[i].price
            i += 1
            total_food_price += food_expenditure

            # Add to the total amount spent
            total_spent += total_food_price

        # FIXME: getting the average spent for food category, handling
        # dividing by zero

        # This is the average amount spent on expenditures in the food category
        try:
            avg_food_expenditures = total_food_price/len(expenditures_food)
        except ZeroDivisionError:
            avg_food_expenditures = "0"

        # Converting the total food price to a string for jinja
        total_food_price = str(total_food_price)

        # Groceries expenditure total
        expenditures_groceries = Expenditure.query.filter_by(category="Groceries", expenditure_userid=id).all()

        # This is total amount spent - it will be increased with every purchase
        total_spent = 0

        # Loop through each item in the food category, add up the prices
        i = 0
        total_groceries_price = 0

        for groceries_expenditure in expenditures_groceries:
            groceries_expenditure = expenditures_groceries[i].price
            i += 1
            total_groceries_price += groceries_expenditure

            # Add to the total amount spent
            total_spent += total_groceries_price

        # This is the average amount spent on expenditures in the groceries category
        try:
            avg_groceries_expenditures = total_groceries_price/len(expenditures_groceries)
        except ZeroDivisionError:
            avg_groceries_expenditures = "0"

        # Converting the total groceries price to a string for jinja
        total_groceries_price = str(total_groceries_price)

        # Travel expenditure total
        expenditures_travel = Expenditure.query.filter_by(category="Travel", expenditure_userid=id).all()

        # Loop through each item in the travel category, add up the prices
        i = 0
        total_travel_price = 0

        for travel_expenditure in expenditures_travel:
            travel_expenditure = expenditures_travel[i].price
            i += 1
            total_travel_price += travel_expenditure

            # Add to the total amount spent
            total_spent += total_travel_price

        # This is the average amount spent on expenditures in the travel category
        try:
            avg_travel_expenditures = total_travel_price/len(expenditures_travel)
        except ZeroDivisionError:
            avg_travel_expenditures = "0"

        # Converting the total travel price to a string for jinja
        total_travel_price = str(total_travel_price)

        # Clothing expenditure total
        expenditures_clothing = Expenditure.query.filter_by(category="Clothing", expenditure_userid=id).all()

        # Loop through each item in the clothing category, add up the prices
        i = 0
        total_clothing_price = 0

        for clothing_expenditure in expenditures_clothing:
            clothing_expenditure = expenditures_clothing[i].price
            i += 1
            total_clothing_price += clothing_expenditure

            # Add to the total amount spent
            total_spent += total_clothing_price

        # This is the average amount spent on expenditures in the clothing category
        try:
            avg_clothing_expenditures = total_clothing_price/len(expenditures_clothing)
        except ZeroDivisionError:
            avg_clothing_expenditures = "0"

        # Converting the total clothing price to a string for jinja
        total_clothing_price = str(total_clothing_price)

        # Entertainment expenditure total
        expenditures_entertainment = Expenditure.query.filter_by(category="Entertainment", expenditure_userid=id).all()

        # Loop through each item in the entertainment category, add up the prices
        i = 0
        total_entertainment_price = 0

        for entertainment_expenditure in expenditures_entertainment:
            entertainment_expenditure = expenditures_entertainment[i].price
            i += 1
            total_entertainment_price += entertainment_expenditure

            # Add to the total amount spent
            total_spent += total_entertainment_price

        # This is the average amount spent on expenditures in the entertainment category
        try:
            avg_entertainment_expenditures = total_entertainment_price/len(expenditures_entertainment)
        except ZeroDivisionError:
            avg_entertainment_expenditures = "0"

        # Converting the total clothing price to a string for jinja
        total_entertainment_price = str(total_entertainment_price)

        # Online purchase expenditure total
        expenditures_online_purchase = Expenditure.query.filter_by(category="Online purchase", expenditure_userid=id).all()

        # Loop through each item in the online purchase category, add up the prices
        i = 0
        total_online_purchase_price = 0

        for online_purchase_expenditure in expenditures_online_purchase:
            online_purchase_expenditure = expenditures_online_purchase[i].price
            i += 1
            total_online_purchase_price += online_purchase_expenditure

            # Add to the total amount spent
            total_spent += total_online_purchase_price

        # This is the average amount spent on expenditures in the online category
        try:
            avg_online_expenditures = total_online_purchase_price/len(expenditures_online_purchase)
        except ZeroDivisionError:
            avg_online_expenditures = "0"

        # Converting the total online price to a string
        total_online_purchase_price = str(total_online_purchase_price)

        ########################################################################
        # END OF CATEGORY TOTAL PRICE CALCULATIONS
        ########################################################################

        # Renders the dashboard, which displays the following info
        return render_template("dashboard.html",
                                                name=user.name,
                                                password=user.password,
                                                email=user.email,
                                                expenditures=expenditures,
                                                id=id,
                                                total_food_price=total_food_price,
                                                total_travel_price=total_travel_price,
                                                total_clothing_price=total_clothing_price,
                                                total_entertainment_price=total_entertainment_price,
                                                total_online_purchase_price=total_online_purchase_price,
                                                total_groceries_price=total_groceries_price,
                                                avg_online_expenditures=avg_online_expenditures,
                                                avg_entertainment_expenditures=avg_entertainment_expenditures,
                                                avg_clothing_expenditures=avg_clothing_expenditures,
                                                avg_travel_expenditures=avg_travel_expenditures,
                                                avg_groceries_expenditures=avg_groceries_expenditures,
                                                avg_food_expenditures=avg_food_expenditures,
                                                total_spent=total_spent,
                                                new_budget=new_budget,
                                                budget_category=budget_category)


@app.route('/expenditure-form', methods=["GET", "POST"])
def expenditure_form():
    """ Add more expenditures on this expenditure form """

    # This is the expenditure form
    return render_template("expenditures-form.html")


@app.route('/budget-form', methods=["GET", "POST"])
def budget_form():
    """ Go to the budget form """

    # This is the budget form
    return render_template("budget.html")


@app.route('/add-budget', methods=["GET", "POST"])
def add_budget():
    """ Add a budget """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    print
    print
    print "id"
    print id
    print

    # Get values from the form
    budget = request.form.get("budget")
    category = request.form.get("category")

    user_budget_query = Budget.query.filter_by(budget_userid=id).all()
    # user_budget_query_cat = user_budget_query.category

    print
    print
    print "user_budget_query"
    print user_budget_query[0].budget_userid
    print
    print user_budget_query[0].category
    print len(user_budget_query)
    print

    for query in user_budget_query:
        if query.category == category:
            print "AHA!"
            print query.category, query.id, query.budget_userid
            db.session.delete(query)
            db.session.commit()

        # else:
        #     print "OH IT'S NEW"
        #     print query.category, query.id, query.budget_userid
            # # Create a new expenditure object to insert into the expenditures table
            # new_budget = Budget(budget=budget,
            #                     category=category,
            #                     budget_userid=id)

            # # Insert the new expenditure into the expenditures table and commit the insert
            # db.session.add(new_budget)
            # db.session.commit()

            print
            print
            print

    new_budget = Budget(budget=budget,
                        category=category,
                        budget_userid=id)

    # Insert the new expenditure into the expenditures table and commit the insert
    db.session.add(new_budget)
    db.session.commit()

    # Redirect to the dashboard
    return redirect(url_for('dashboard',
                             id=id))
                             # new_budget=new_budget))


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


@app.route('/remove-expenditure/<int:id>', methods=["GET", "POST"])
def remove_expenditure(id):
    """ Remove an expenditure from the database """

    # This is the expenditure object we are working with
    # FIXME: expenditure_at_hand and expenditure_stuff are the same. Fix this!
    expenditure_at_hand = Expenditure.query.filter_by(id=id).first()

    # This queries for the id of the user tied to the expenditure
    expenditure_id = expenditure_at_hand.expenditure_userid

    # This queries the expenditure details
    expenditure_stuff = Expenditure.query.filter_by(id=id).first()

    # Deletes the expenditure item from the expenditure table
    db.session.delete(expenditure_stuff)
    db.session.commit()

    # Redirect the user to their dashboard
    return redirect(url_for('dashboard', id=expenditure_id))


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
