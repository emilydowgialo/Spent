from jinja2 import StrictUndefined

# from pprint import pprint

from datetime import datetime, timedelta

import requests

from flask import Flask, request, render_template, session, url_for, flash, redirect, jsonify, json, abort
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db, db, Expenditure, Budget

from tools import expenditure_function, budget_totals, get_dates_for_budget, get_progress, get_budget_per_category

from sqlalchemy.sql import and_

import os

import hashlib

import hmac

import base64

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app = Flask(__name__, instance_relative_config=True)

app.secret_key = os.getenv('SECRET_KEY')

spent_database = os.getenv('POSTGRES_DB_URL')
connect_to_db(app, spent_database)


@app.route('/')
def index():
    """ Homepage """

    APP_ID = os.getenv('APP_ID')    

    # This is the homepage
    return render_template("homepage.html", user_session_info=session,
                                            app_id=APP_ID)


@app.route('/profile-edit', methods=["POST"])
def profile_edit():
    """ Edit profile information """

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Query the database for the user
    user_info = User.query.filter_by(id=id).first()

    # Get information from the forms
    name = request.form.get("profile-name")
    email = request.form.get("profile-email")
    password = request.form.get("new-password")

    # Replace info in the database with new info
    if name:
        user_info.name = name
        db.session.commit()

    if password:
        user_info.password = password
        db.session.commit()

    if email:
        user_info.email = email
        db.session.commit()

    name_info = {
        'name': name,
        'email': email
    }

    # Return jsonified budget info to submit-new-account-info.js
    return jsonify(name_info)


@app.route('/webhook', methods=['POST'])
def intercom_webhook():

    x_signature_header = request.headers['X-Hub-Signature']

    print 
    print
    print
    print x_signature_header
    print
    print
    print

    json_blob = request.data

    print
    print
    print
    print json_blob
    print
    print
    print

    KEY = os.getenv('MARSH_SECRET')

    print
    print type(KEY)
    print "yo"
    print "hi"
    print

    hash_result = hmac.new(KEY, json_blob, hashlib.sha1).hexdigest()

    print
    print "hi"
    print
    print type(hash_result)
    print hash_result
    print "sha1=" + hash_result
    print

    if "sha1=" + hash_result == x_signature_header:

        print
        print
        print "cool"
        print
        print

        return 'OK'

    else:

        print
        print
        print "bad"
        print
        print

        return abort (400)


@app.route('/tracking/<tracking_num>', methods=["POST"])
def tracking_with_id(tracking_num):
    """ Handle the tracking information and display on the map """

    # Get the expenditure associated with the tracking number
    expenditure_object = Expenditure.query.filter_by(tracking_num=tracking_num).first()

    # Get the carrier associated with the tracking number
    carrier = expenditure_object.tracking_num_carrier

    def shippo_url(track_num, carrier_info):
        """ Creates API call using tracking information the user input via the form """

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

    # This is the delivery status of the paackage
    tracking_status = data['tracking_status']['status']

    address_info = {
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'country': country,
        'tracking_status': tracking_status
    }

    # Return jsonified budget info to map.js
    return jsonify(address_info)


@app.route('/total-spent.json')
def budget_types_data():
    """ Bar chart shows totals for last 30 days """

    id = session.get('id')

    # This is today's date
    today = datetime.today().strftime('%Y-%m-%d')
    # '2016-05-31'

    # This is the date 30 days in the past from today
    thirty_days_past = (datetime.today() + timedelta(-30)).strftime('%Y-%m-%d')

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function(3, id, thirty_days_past, today)
        total_groceries_price, avg_groceries_expenditures = expenditure_function(4, id, thirty_days_past, today)
        total_clothing_price, avg_clothing_expenditures = expenditure_function(5, id, thirty_days_past, today)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function(6, id, thirty_days_past, today)
        total_travel_price, avg_travel_expenditures = expenditure_function(2, id, thirty_days_past, today)
        total_online_purchase_price, avg_online_expenditures = expenditure_function(1, id, thirty_days_past, today)

    data_dict = {
        "labels": ["Food", "Groceries", "Clothing", "Entertainment", "Travel", "Online Purchases"],
        "datasets": [
            {
                "label": "Total Spent",
                "fillColor": "#F37257",
                "strokeColor": "#F37257",
                "pointColor": "#F37257",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "#F37257",
                "data": [total_food_price, total_groceries_price, total_clothing_price, total_entertainment_price, total_travel_price, total_online_purchase_price]
            },
            {
                "label": "Average",
                "fillColor": "#AFC1CC",
                "strokeColor": "#AFC1CC",
                "pointColor": "#AFC1CC",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "#AFC1CC",
                "data": [avg_food_expenditures, avg_groceries_expenditures, avg_clothing_expenditures, avg_entertainment_expenditures, avg_travel_expenditures, avg_online_expenditures]
            }
        ]
    }

    # This returns the data jsonified
    return jsonify(data_dict)


@app.route('/expenditure-types.json')
def expenditure_types_data():
    """ Return data about expenditures to the donut chart """

    # Get the id of the user in the session
    id = session.get('id')

    # This is today's date
    today = datetime.today().strftime('%Y-%m-%d')
    # '2016-05-31'

    # This is the date 30 days in the past from today
    thirty_days_past = (datetime.today() + timedelta(-30)).strftime('%Y-%m-%d')

    # Get the total amount spent per category by calling the get_expenditures function
    travel_expenditures, avg_travel = expenditure_function(2, id, thirty_days_past, today)
    entertainment_expenditures, avg_entertainment = expenditure_function(6, id, thirty_days_past, today)
    groceries_expenditures, avg_groceries = expenditure_function(4, id, thirty_days_past, today)
    clothing_expenditures, avg_clothing = expenditure_function(5, id, thirty_days_past, today)
    food_expenditures, avg_food = expenditure_function(3, id, thirty_days_past, today)
    online_purchase_expenditures, avg_online = expenditure_function(1, id, thirty_days_past, today)

    # Jsonified info
    data_list_of_dicts = {
        'expenditures': [
            {
                "value": travel_expenditures,
                "color": "#F4D27A",
                "highlight": "#963019",
                "label": "Travel"
            },
            {
                "value": entertainment_expenditures,
                "color": "#517281",
                "highlight": "#963019",
                "label": "Entertainment"
            },
            {
                "value": groceries_expenditures,
                "color": "#7895A2",
                "highlight": "#963019",
                "label": "Groceries"
            },
            {
                "value": clothing_expenditures,
                "color": "#AFC1CC",
                "highlight": "#963019",
                "label": "Clothing"
            },
            {
                "value": food_expenditures,
                "color": "#F37257",
                "highlight": "#963019",
                "label": "Food"
            },
            {
                "value": online_purchase_expenditures,
                "color": "#F68D5C",
                "highlight": "#963019",
                "label": "Online Purchase"
            }
        ]
    }

    # Return jsonified info
    return jsonify(data_list_of_dicts)


@app.route('/dashboard/<int:id>')
def dashboard(id):
    """ This is the user dashboard """

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:

        # This is the user object
        user = User.query.filter_by(id=id).first()

        ### GENERATE THE USER HASH ###

        APP_ID = os.getenv('APP_ID')
        KEY = os.getenv('SECURE_MODE_KEY')
        MESSAGE = str(user.id)
        hash_result = hmac.new(KEY, MESSAGE, hashlib.sha256).hexdigest() 

        ####### GET THE USER'S BUDGETS FOR EACH CATEGORY

        cat_1_budget = get_budget_per_category(1, id)
        cat_2_budget = get_budget_per_category(2, id)
        cat_3_budget = get_budget_per_category(3, id)
        cat_4_budget = get_budget_per_category(4, id)
        cat_5_budget = get_budget_per_category(5, id)
        cat_6_budget = get_budget_per_category(6, id)

        # This is the expenditure object, which contains information about
        # expenditures specific to the user from the expenditure table in the
        # database
        expenditures = Expenditure.query.filter_by(expenditure_userid=id).all()

        ########### GET BUDGET START AND END DATES ###########

        # Calls the get_dates_for_budget function in tools.py
        cat_3_start, cat_3_end = get_dates_for_budget(3, id)
        cat_1_start, cat_1_end = get_dates_for_budget(1, id)
        cat_2_start, cat_2_end = get_dates_for_budget(2, id)
        cat_4_start, cat_4_end = get_dates_for_budget(4, id)
        cat_5_start, cat_5_end = get_dates_for_budget(5, id)
        cat_6_start, cat_6_end = get_dates_for_budget(6, id)

        # Strips datetime objects to year, month, day
        cat_3_start_date = cat_3_start.strftime('%m-%d-%Y')
        cat_1_start_date = cat_1_start.strftime('%m-%d-%Y')
        cat_2_start_date = cat_2_start.strftime('%m-%d-%Y')
        cat_4_start_date = cat_4_start.strftime('%m-%d-%Y')
        cat_5_start_date = cat_5_start.strftime('%m-%d-%Y')
        cat_6_start_date = cat_6_start.strftime('%m-%d-%Y')

        cat_3_end_date = cat_3_end.strftime('%m-%d-%Y')
        cat_1_end_date = cat_1_end.strftime('%m-%d-%Y')
        cat_2_end_date = cat_2_end.strftime('%m-%d-%Y')
        cat_4_end_date = cat_4_end.strftime('%m-%d-%Y')
        cat_5_end_date = cat_5_end.strftime('%m-%d-%Y')
        cat_6_end_date = cat_6_end.strftime('%m-%d-%Y')

        ########### TOTAL PRICE AND AVERAGE SPENT ###########

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function(3, id, cat_3_start_date, cat_3_end_date)
        total_groceries_price, avg_groceries_expenditures = expenditure_function(4, id, cat_4_start_date, cat_4_end_date)
        total_clothing_price, avg_clothing_expenditures = expenditure_function(5, id, cat_5_start_date, cat_5_end_date)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function(6, id, cat_6_start_date, cat_6_end_date)
        total_travel_price, avg_travel_expenditures = expenditure_function(2, id, cat_2_start_date, cat_2_end_date)
        total_online_purchase_price, avg_online_expenditures = expenditure_function(1, id, cat_1_start_date, cat_1_end_date)

        total_price = (total_food_price + total_groceries_price + total_clothing_price +
                       total_entertainment_price + total_travel_price +
                       total_online_purchase_price)

        ########### BUDGET ###########

        # Calling the function for each of the expenditure categories
        food_budget_minus_expenses = budget_totals(3, id, total_food_price)
        online_budget_minus_expenses = budget_totals(1, id, total_online_purchase_price)
        groceries_budget_minus_expenses = budget_totals(4, id, total_groceries_price)
        clothing_budget_minus_expenses = budget_totals(5, id, total_clothing_price)
        travel_budget_minus_expenses = budget_totals(2, id, total_travel_price)
        entertainment_budget_minus_expenses = budget_totals(6, id, total_entertainment_price)

        ############# PROGRESS BAR ##############

        # Call get_progress in tools.py to calculate the progress bar totals
        clothing_progress = get_progress(clothing_budget_minus_expenses, cat_5_budget)
        online_progress = get_progress(online_budget_minus_expenses, cat_1_budget)
        food_progress = get_progress(food_budget_minus_expenses, cat_3_budget)
        groceries_progress = get_progress(groceries_budget_minus_expenses, cat_4_budget)
        entertainment_progress = get_progress(entertainment_budget_minus_expenses, cat_6_budget)
        travel_progress = get_progress(travel_budget_minus_expenses, cat_2_budget)

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
                                                cat_1_budget=cat_1_budget,
                                                cat_2_budget=cat_2_budget,
                                                cat_3_budget=cat_3_budget,
                                                cat_4_budget=cat_4_budget,
                                                cat_5_budget=cat_5_budget,
                                                cat_6_budget=cat_6_budget,
                                                cat_1_start_date=cat_1_start_date,
                                                cat_2_start_date=cat_2_start_date,
                                                cat_3_start_date=cat_3_start_date,
                                                cat_4_start_date=cat_4_start_date,
                                                cat_5_start_date=cat_5_start_date,
                                                cat_6_start_date=cat_6_start_date,
                                                cat_1_end_date=cat_1_end_date,
                                                cat_2_end_date=cat_2_end_date,
                                                cat_3_end_date=cat_3_end_date,
                                                cat_4_end_date=cat_4_end_date,
                                                cat_5_end_date=cat_5_end_date,
                                                cat_6_end_date=cat_6_end_date,
                                                clothing_progress=clothing_progress,
                                                entertainment_progress=entertainment_progress,
                                                online_progress=online_progress,
                                                food_progress=food_progress,
                                                groceries_progress=groceries_progress,
                                                travel_progress=travel_progress,
                                                total_price=total_price,
                                                user_hash=hash_result,
                                                app_id=APP_ID)


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
    start_date = request.form.get("start-date")
    end_date = request.form.get("end-date")

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
                        budget_userid=id,
                        budget_start_date=start_date,
                        budget_end_date=end_date)

    # Insert the new budget into the budget table and commit the insert
    db.session.add(new_budget)
    db.session.commit()

    # Call functions in tools.py
    total_cat_price, avg_cat_expenditures = expenditure_function(category_id, id, start_date, end_date)
    cat_budget_minus_expenses = budget_totals(category_id, id, total_cat_price)

    # Call get_progress in tools.py to calculate the progress bar totals
    category_progress = get_progress(cat_budget_minus_expenses, budget)

    budget_info = {
        'id': new_budget.id,
        'category': new_budget.category.category,
        'category_id': category_id,
        'budget': budget,
        'cat_budget_minus_expenses': cat_budget_minus_expenses,
        'category_progress': category_progress
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
    tracking_num = request.form.get("tracking-num")
    tracking_num_carrier = request.form.get("tracking-num-carrier")

    start_date, end_date = get_dates_for_budget(category_id, id)

    # Create a new expenditure object to insert into the expenditures table
    new_expenditure = Expenditure(category_id=category_id,
                                  price=price,
                                  date_of_expenditure=date_of_expenditure,
                                  where_bought=where_bought,
                                  description=description,
                                  expenditure_userid=id,
                                  tracking_num=tracking_num,
                                  tracking_num_carrier=tracking_num_carrier)

    # Insert the new expenditure into the expenditures table and commit the insert
    db.session.add(new_expenditure)
    db.session.commit()

    # Unpacking the function call
    total_cat_price, avg_cat_expenditures = expenditure_function(category_id, id, start_date, end_date)

    budget_minus_expenses = budget_totals(category_id, id, total_cat_price)
    cat_budget = get_budget_per_category(category_id, id)
    category_progress = get_progress(budget_minus_expenses, cat_budget)

    expenditure_info = {
        'total_cat_price': total_cat_price,
        'avg_cat_expenditures': avg_cat_expenditures,
        'category_id': category_id,
        'expenditure_id': new_expenditure.id,
        'date_of_expenditure': new_expenditure.date_of_expenditure.strftime('%Y-%m-%d'),
        'where_bought': new_expenditure.where_bought,
        'description': new_expenditure.description,
        'price': str(new_expenditure.price),
        'category': new_expenditure.category.category,
        'tracking_num': new_expenditure.tracking_num,
        'tracking_num_carrier': new_expenditure.tracking_num_carrier,
        'cat_budget_minus_expenses': budget_minus_expenses,
        'category_progress': category_progress
    }

    # Return jsonified info to submit-expenditure.js
    return jsonify(expenditure_info)


@app.route('/remove-expenditure/<int:id>', methods=["POST"])
def remove_expenditure(id):
    """ Remove an expenditure from the database """

    # This is the expenditure object we are working with
    expenditure_at_hand = Expenditure.query.filter_by(id=id).first()

    # Deletes the expenditure item from the expenditure table
    db.session.delete(expenditure_at_hand)
    db.session.commit()

    # Return jsonified id to delete-expenditure.js
    return jsonify({"expenditure_id": id})


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


@app.route('/logout', methods=["GET"])
def logout():
    """ Logs the user out """

    # Remove the user id from the session if it exists
    session.pop('id', None)

    # Bring the user back to the homepage once they have been logged out
    return redirect(url_for('index'))


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # spent_database = 'postgres:///spending'
    # connect_to_db(app, spent_database)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
