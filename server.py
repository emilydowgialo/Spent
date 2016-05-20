from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, url_for, flash, redirect, jsonify
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


@app.route('/chart-test', methods=["POST"])
def chart_test():
    """ Testing the charts """

    # This is the test chart page
    return render_template("charttest.html")


@app.route('/total-spent.json')
def budget_types_data():
    """ Bar chart """

    id = session.get('id')

    # If the user id is in the session, this will render the dashboard
    # template, which will display their information and expenditure information
    if 'id' in session:

        # The following function gets the total amount and average amount spent
        def expenditure_function(category, id):
            """ Calculate the total amount and avg spent in one particular category """

            # List of expenditure objects
            expenditures = Expenditure.query.filter_by(category=category, expenditure_userid=id).all()

            # Initialize the total price at 0
            total_price = 0

            # Increase the total price by the price of each expenditure
            for expenditure in expenditures:
                expenditure_price = expenditure.price
                total_price += expenditure_price

            # This gets the average price; if there is an error due to no
            # expenditures, it returns the value of "0"
            try:
                avg_expenditures = total_price/len(expenditures)
            except ZeroDivisionError:
                avg_expenditures = "0"

            return float(total_price), float(avg_expenditures)

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function("Food", id)
        total_groceries_price, avg_groceries_expenditures = expenditure_function("Groceries", id)
        total_clothing_price, avg_clothing_expenditures = expenditure_function("Clothing", id)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function("Entertainment", id)
        total_travel_price, avg_travel_expenditures = expenditure_function("Travel", id)
        total_online_purchase_price, avg_online_expenditures = expenditure_function("Online Purchase", id)

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

    id = session.get('id')

    def get_expenditures(category, id):

        expenditures = Expenditure.query.filter_by(category=category, expenditure_userid=id).all()

        expenditure_list = []
        for expenditure in expenditures:
            expenditure = expenditure.price
            expenditure_list.append(expenditure)

        expenditure_total = int(sum(expenditure_list))
        return expenditure_total

    travel_expenditures = get_expenditures("Travel", id)
    entertainment_expenditures = get_expenditures("Entertainment", id)
    groceries_expenditures = get_expenditures("Groceries", id)
    clothing_expenditures = get_expenditures("Clothing", id)
    food_expenditures = get_expenditures("Food", id)
    online_purchase_expenditures = get_expenditures("Online Purchase", id)

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

    return jsonify(data_list_of_dicts)


@app.route('/dashboard/<int:id>')
def dashboard(id):
    """ This is the user dashboard """

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

        # The following function gets the total amount and average amount spent
        def expenditure_function(category, id):
            """ Calculate the total amount and avg spent in one particular category """

            # List of expenditure objects
            expenditures = Expenditure.query.filter_by(category=category, expenditure_userid=id).all()

            # Initialize the total price at 0
            total_price = 0

            # Increase the total price by the price of each expenditure
            for expenditure in expenditures:
                expenditure_price = expenditure.price
                total_price += expenditure_price

            # This gets the average price; if there is an error due to no
            # expenditures, it returns the value of "0"
            try:
                avg_expenditures = total_price/len(expenditures)
            except ZeroDivisionError:
                avg_expenditures = "0"

            return str(total_price), str(avg_expenditures)

        # Unpacking the total price and average spent
        total_food_price, avg_food_expenditures = expenditure_function("Food", id)
        total_groceries_price, avg_groceries_expenditures = expenditure_function("Groceries", id)
        total_clothing_price, avg_clothing_expenditures = expenditure_function("Clothing", id)
        total_entertainment_price, avg_entertainment_expenditures = expenditure_function("Entertainment", id)
        total_travel_price, avg_travel_expenditures = expenditure_function("Travel", id)
        total_online_purchase_price, avg_online_expenditures = expenditure_function("Online Purchase", id)
        total_price = (float(total_food_price) + float(total_groceries_price) + float(total_clothing_price) +
                       float(total_entertainment_price) + float(total_travel_price) +
                       float(total_online_purchase_price))

        # The following functon gets the budget minus expenditures
        def budget_totals(category, id, total_price):
            """ Calculate budget minus expenditures made """

            # This is the expenditure object
            expenditure_budget = Budget.query.filter_by(category=category, budget_userid=id).first()

            # Initializes the budget at 0
            expenditure_budget_minus_expenses = 0

            # If there is a budget, this subtracts the total expenses from it, or
            # returns a statement about the user not inputting a budget yet
            if expenditure_budget is not None:
                budget_total = expenditure_budget.budget
                expenditure_budget_minus_expenses = float(budget_total) - float(total_price)

            else:
                expenditure_budget_minus_expenses = "You haven't added a budget yet"

            return expenditure_budget_minus_expenses

        # Calling the function for each of the expenditure categories
        food_budget_minus_expenses = budget_totals("Food", id, total_food_price)
        online_budget_minus_expenses = budget_totals("Online Purchase", id, total_online_purchase_price)
        groceries_budget_minus_expenses = budget_totals("Groceries", id, total_groceries_price)
        clothing_budget_minus_expenses = budget_totals("Clothing", id, total_clothing_price)
        travel_budget_minus_expenses = budget_totals("Travel", id, total_travel_price)
        entertainment_budget_minus_expenses = budget_totals("Entertainment", id, total_entertainment_price)

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


@app.route('/expenditure-form', methods=["POST"])
def expenditure_form():
    """ Add more expenditures on this expenditure form """

    # This is the expenditure form
    return render_template("expenditures-form.html")


@app.route('/budget-form', methods=["POST"])
def budget_form():
    """ Go to the budget form """

    # This is the budget form
    return render_template("budget.html")


@app.route('/budget-testing', methods=["POST"])
def budget_form_testing():
    """ Go to the budget form """

    # This is the budget form
    return render_template("form-test.html")


@app.route('/remove-budget/<int:id>', methods=["POST"])
def remove_budget(id):
    """ Remove a budget from the database """

    # This is the budget object we are working with
    budget_at_hand = Budget.query.filter_by(id=id).first()

    # This queries for the id of the user tied to the budget
    budget_id = budget_at_hand.budget_userid

    # Deletes the budget item from the budget table
    db.session.delete(budget_at_hand)
    db.session.commit()

    # Redirect the user to their dashboard
    return redirect(url_for('dashboard', id=budget_id))


@app.route('/add-budget-test', methods=["POST"])
def add_budget_test():

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Get values from the form
    budget = request.form.get("budget-test")
    category = request.form.get("category-test")

    print
    print request.form
    print "form stuff"
    print budget
    print category
    print
    print

    user_budget_query = Budget.query.filter_by(budget_userid=id).all()

    # Check for budgets in the database under the user ID in particular categories;
    # delete budgets that exist to override them
    # Check to see if you can modify it instead
    for query in user_budget_query:
        if query.category == category:
            db.session.delete(query)
            db.session.commit()

    # Add the budget to the database. It will be the only budget for that
    # category in the database for the user
    new_budget = Budget(budget=budget,
                        category=category,
                        budget_userid=id)

    # Insert the new budget into the budget table and commit the insert
    db.session.add(new_budget)
    db.session.commit()

    print
    print
    print "new_budget"
    print new_budget
    print
    print

    budget_info = {
        'category': category,
        'budget': budget
    }

    print
    print
    print "budget_info"
    print budget_info
    print
    print

    # Redirect to the dashboard
    return jsonify(budget_info)
    # redirect(url_for('dashboard', id=id))


@app.route('/add-budget', methods=["POST"])
def add_budget():
    """ Add a budget """

    # # Set the value of the user id of the user in the session
    # id = session.get('id')

    # # Get values from the form
    # budget = request.form.get("budget")
    # category = request.form.get("category")

    # user_budget_query = Budget.query.filter_by(budget_userid=id).all()

    # # Check for budgets in the database under the user ID in particular categories;
    # # delete budgets that exist to override them
    # # Check to see if you can modify it instead
    # for query in user_budget_query:
    #     if query.category == category:
    #         db.session.delete(query)
    #         db.session.commit()

    # # Add the budget to the database. It will be the only budget for that
    # # category in the database for the user
    # new_budget = Budget(budget=budget,
    #                     category=category,
    #                     budget_userid=id)

    # # Insert the new budget into the budget table and commit the insert
    # db.session.add(new_budget)
    # db.session.commit()

    # # Redirect to the dashboard
    # return "Budget added"
    # # redirect(url_for('dashboard', id=id))

    # Set the value of the user id of the user in the session
    id = session.get('id')

    # Get values from the form
    budget = request.form.get("budget")
    category = request.form.get("category")

    print
    print request.form
    print "form stuff"
    print budget
    print category
    print
    print

    user_budget_query = Budget.query.filter_by(budget_userid=id).all()

    # Check for budgets in the database under the user ID in particular categories;
    # delete budgets that exist to override them
    # Check to see if you can modify it instead
    for query in user_budget_query:
        if query.category == category:
            db.session.delete(query)
            db.session.commit()

    # Add the budget to the database. It will be the only budget for that
    # category in the database for the user
    new_budget = Budget(budget=budget,
                        category=category,
                        budget_userid=id)

    # Insert the new budget into the budget table and commit the insert
    db.session.add(new_budget)
    db.session.commit()

    print
    print
    print "new_budget"
    print new_budget
    print
    print

    budget_info = {
        'category': category,
        'budget': budget
    }

    print
    print
    print "budget_info"
    print budget_info
    print
    print

    # Redirect to the dashboard
    return jsonify(budget_info)
    # redirect(url_for('dashboard', id=id))


@app.route('/add-expenditure-to-db', methods=["POST"])
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
    return "congrats"
    # redirect(url_for('dashboard', id=id))


@app.route('/remove-expenditure/<int:id>', methods=["POST"])
def remove_expenditure(id):
    """ Remove an expenditure from the database """

    # This is the expenditure object we are working with
    expenditure_at_hand = Expenditure.query.filter_by(id=id).first()

    # This queries for the id of the user tied to the expenditure
    expenditure_id = expenditure_at_hand.expenditure_userid

    # Deletes the expenditure item from the expenditure table
    db.session.delete(expenditure_at_hand)
    db.session.commit()

    # Redirect the user to their dashboard
    return redirect(url_for('dashboard', id=expenditure_id))


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
