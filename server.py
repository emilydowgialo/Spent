from jinja2 import StrictUndefined

# from pprint import pprint

import requests

from flask import Flask, request, render_template, session, url_for, flash, redirect, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db, Expenditure, Budget

from tools import expenditure_function, budget_totals

from sqlalchemy.sql import and_

app = Flask(__name__)

app.secret_key = "CATS123"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage """

    # This is the homepage
    return render_template("homepage.html", user_session_info=session)


@app.route('/edit-profile', methods=["POST"])
def edit_profile():
    """ Go to the profile edit page """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # This is the user object
    user = User.query.filter_by(id=id).first()

    return render_template("edit-profile.html", user=user)


@app.route('/profile-edit', methods=["POST"])
def profile_edit():
    """ Edit profile information """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Query the database for the user
    user_info = User.query.filter_by(id=id).first()

    # Get information from the forms
    name = request.form.get("name")
    password = request.form.get("password")

    # Replace info in the database with new info
    if name:
        user_info.name = name
        db.session.commit()

    else:
        user_info.password = password
        db.session.commit()

    return redirect(url_for('dashboard', id=id))


@app.route('/tracking', methods=["POST"])
def tracking():

    # Tracking number and carrier
    tracking_num = request.form.get("tracking-number")
    carrier = request.form.get("carrier")

    def shippo_url(track_num, carrier_info):
        """ Creates api call using tracking information the user input via the form """

        url = "https://api.goshippo.com/v1/tracks/" + str(carrier_info) + "/" + str(track_num) + "/"
        return url

    # Returns the data we need
    shippo_tracking = shippo_url(tracking_num, carrier)
    result = requests.get(shippo_tracking)
    data = json.loads(result.content)

    final_dest = data['tracking_status']['location']

    city = final_dest['city']
    state = final_dest['state']
    zipcode = final_dest['zip']
    country = final_dest['country']

    address_info = {
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'country': country
    }

    # Return jsonified budget info to the map
    return jsonify(address_info)


@app.route('/total-spent.json')
def budget_types_data():
    """ Bar chart """

    id = session.get('id')

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function(3, id)
        total_groceries_price, avg_groceries_expenditures = expenditure_function(4, id)
        total_clothing_price, avg_clothing_expenditures = expenditure_function(5, id)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function(6, id)
        total_travel_price, avg_travel_expenditures = expenditure_function(2, id)
        total_online_purchase_price, avg_online_expenditures = expenditure_function(1, id)

    data_dict = {
        "labels": ["Food", "Groceries", "Clothing", "Entertainment", "Travel", "Online Purchase"],
        "datasets": [
            {
                "label": "Total Spent",
                "fillColor": "rgba(220,220,220,0.2)",
                "strokeColor": "rgba(220,220,220,1)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(220,220,220,1)",
                "data": [total_food_price, total_groceries_price, total_clothing_price, total_entertainment_price, total_travel_price, total_online_purchase_price]
            },
            {
                "label": "Average",
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)",
                "data": [avg_food_expenditures, avg_groceries_expenditures, avg_clothing_expenditures, avg_entertainment_expenditures, avg_travel_expenditures, avg_online_expenditures]
            }
        ]
    }

    # This returns the data jsonified
    return jsonify(data_dict)


@app.route('/expenditure-types.json')
def expenditure_types_data():
    """ Return data about expenditures """

    # Get the id of the user in the session
    id = session.get('id')

    def get_expenditures(category_id, id):
        """ Gets a list of expenditure prices """

        expenditures = Expenditure.query.filter_by(category_id=category_id, expenditure_userid=id).all()

        expenditure_list = []
        for expenditure in expenditures:
            expenditure = expenditure.price
            expenditure_list.append(expenditure)

        expenditure_total = int(sum(expenditure_list))
        return expenditure_total

    # Get the total amount spent per category by calling the get_expenditures function
    travel_expenditures = get_expenditures(2, id)
    entertainment_expenditures = get_expenditures(6, id)
    groceries_expenditures = get_expenditures(4, id)
    clothing_expenditures = get_expenditures(5, id)
    food_expenditures = get_expenditures(3, id)
    online_purchase_expenditures = get_expenditures(1, id)

    # Jsonified info
    data_list_of_dicts = {
        'expenditures': [
            {
                "value": travel_expenditures,
                "color": "#F7464A",
                "highlight": "#FF5A5E",
                "label": "Travel"
            },
            {
                "value": entertainment_expenditures,
                "color": "#46BFBD",
                "highlight": "#5AD3D1",
                "label": "Entertainment"
            },
            {
                "value": groceries_expenditures,
                "color": "#4dff4d",
                "highlight": "#5AD3D1",
                "label": "Groceries"
            },
            {
                "value": clothing_expenditures,
                "color": "#bf80ff",
                "highlight": "#5AD3D1",
                "label": "Clothing"
            },
            {
                "value": food_expenditures,
                "color": "#ffcc80",
                "highlight": "#5AD3D1",
                "label": "Food"
            },
            {
                "value": online_purchase_expenditures,
                "color": "blue",
                "highlight": "#FFC870",
                "label": "Online Purchase"
            }
        ]
    }

    # Return jsonified info
    return jsonify(data_list_of_dicts)


@app.route('/dashboard/<int:id>')
def dashboard(id):
    """ This is the user dashboard """

    # TO FIX: make it so you can't view other dashboards

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:

        # This is the user object
        user = User.query.filter_by(id=id).first()

        # This is the user's budget
        budget = Budget.query.filter_by(budget_userid=id).all()

        # This is the expenditure object, which contains information about
        # expenditures specific to the user from the expenditure table in the
        # database
        expenditures = Expenditure.query.filter_by(expenditure_userid=id).all()

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function(3, id)
        total_groceries_price, avg_groceries_expenditures = expenditure_function(4, id)
        total_clothing_price, avg_clothing_expenditures = expenditure_function(5, id)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function(6, id)
        total_travel_price, avg_travel_expenditures = expenditure_function(2, id)
        total_online_purchase_price, avg_online_expenditures = expenditure_function(1, id)
        total_price = (total_food_price + total_groceries_price + total_clothing_price +
                       total_entertainment_price + total_travel_price +
                       total_online_purchase_price)

        # Calling the function for each of the expenditure categories
        food_budget_minus_expenses = budget_totals(3, id, total_food_price)
        online_budget_minus_expenses = budget_totals(1, id, total_online_purchase_price)
        groceries_budget_minus_expenses = budget_totals(4, id, total_groceries_price)
        clothing_budget_minus_expenses = budget_totals(5, id, total_clothing_price)
        travel_budget_minus_expenses = budget_totals(2, id, total_travel_price)
        entertainment_budget_minus_expenses = budget_totals(6, id, total_entertainment_price)

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
                                                clothing_budget_minus_expenses=clothing_budget_minus_expenses,
                                                travel_budget_minus_expenses=travel_budget_minus_expenses,
                                                groceries_budget_minus_expenses=groceries_budget_minus_expenses,
                                                food_budget_minus_expenses=food_budget_minus_expenses,
                                                online_budget_minus_expenses=online_budget_minus_expenses,
                                                entertainment_budget_minus_expenses=entertainment_budget_minus_expenses,
                                                total_price=total_price,
                                                budget=budget)


@app.route('/remove-budget/<int:id>', methods=["POST"])
def remove_budget(id):
    """ Remove a budget from the database """

    # This is the budget object we are working with
    budget_at_hand = Budget.query.filter_by(id=id).first()

    # This is the user id of the user in the session
    user_id = session.get('id')

    # Check to make sure the budget is associated with the logged in user
    if user_id == budget_at_hand.budget_userid:

        # Deletes the budget item from the budget table
        db.session.delete(budget_at_hand)
        db.session.commit()

    # Redirect the user to their dashboard
    return redirect(url_for('dashboard', id=user_id))


@app.route('/add-budget', methods=["POST"])
def add_budget():
    """ Add a budget """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Get values from the form
    budget = request.form.get("budget")
    category_id = int(request.form.get("category"))

    user_budget_query = Budget.query.filter_by(budget_userid=id).all()

    # Check for budgets in the database under the user ID in particular categories;
    # delete budgets that exist to override them
    # Check to see if you can modify it instead
    for query in user_budget_query:
        if query.category_id == category_id:
            db.session.delete(query)
            db.session.commit()

    # Add the budget to the database. It will be the only budget for that
    # category in the database for the user
    new_budget = Budget(budget=budget,
                        category_id=category_id,
                        budget_userid=id)

    # Insert the new budget into the budget table and commit the insert
    db.session.add(new_budget)
    db.session.commit()

    total_cat_price, avg_cat_expenditures = expenditure_function(category_id, id)
    cat_budget_minus_expenses = budget_totals(category_id, id, total_cat_price)

    budget_info = {
        'id': new_budget.id,
        'category': new_budget.category.category,
        'category_id': category_id,
        'budget': budget,
        'cat_budget_minus_expenses': cat_budget_minus_expenses
    }

    # Return jsonified budget info to submit-budget.js
    return jsonify(budget_info)


@app.route('/add-expenditure-to-db', methods=["POST"])
def add_expenditure():
    """ Add new expenditure to the database """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Get values from the form
    category_id = int(request.form.get("category"))
    price = request.form.get("price")
    date_of_expenditure = request.form.get("date")
    where_bought = request.form.get("wherebought")
    description = request.form.get("description")

    # Create a new expenditure object to insert into the expenditures table
    new_expenditure = Expenditure(category_id=category_id,
                                  price=price,
                                  date_of_expenditure=date_of_expenditure,
                                  where_bought=where_bought,
                                  description=description,
                                  expenditure_userid=id)

    # Insert the new expenditure into the expenditures table and commit the insert
    db.session.add(new_expenditure)
    db.session.commit()

    # Unpacking the function call
    total_cat_price, avg_cat_expenditures = expenditure_function(category_id, id)

    expenditure_info = {
        'total_cat_price': total_cat_price,
        'avg_cat_expenditures': avg_cat_expenditures,
        'category_id': category_id,
        'expenditure_id': new_expenditure.id,
        'date_of_expenditure': new_expenditure.date_of_expenditure,
        'where_bought': new_expenditure.where_bought,
        'description': new_expenditure.description,
        'price': str(new_expenditure.price),
        'category': new_expenditure.category.category,
    }

    # Return jsonified info to submit-expenditure.js
    return jsonify(expenditure_info)


@app.route('/remove-expenditure/<int:id>', methods=["POST"])
def remove_expenditure(id):
    """ Remove an expenditure from the database """

    # This is the expenditure object we are working with
    expenditure_at_hand = Expenditure.query.filter_by(id=id).first()

    user_id = session.get('id')

    # Deletes the expenditure item from the expenditure table
    db.session.delete(expenditure_at_hand)
    db.session.commit()

    # Redirect the user to their dashboard
    return redirect(url_for('dashboard', id=user_id))


@app.route('/sign-up-form', methods=["POST"])
def sign_up_form():
    """ Sign up form """

    # Takes the user to the signup page
    return render_template("signup.html")


@app.route('/sign-up', methods=["POST"])
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


@app.route('/login', methods=["POST"])
def login():
    """ Directs the user to the login form """

    # Take the user to the login page
    return render_template("login.html")


@app.route('/login-form', methods=["POST"])
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


@app.route('/logout', methods=["POST"])
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
