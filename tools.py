from model import Expenditure, Budget

from datetime import datetime


########## THIS FILE CONTAINS WIDELY USED FUNCTIONS ###########


def expenditure_function(category_id, id, start, end):
    """ Calculate the total amount and avg spent in one particular category """

    # List of expenditure objects
    expenditures = Expenditure.query.filter_by(
        category_id=category_id, expenditure_userid=id).filter(
        Expenditure.date_of_expenditure.between(start, end)).all()

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


def get_dates_for_budget(category_id, id):
    """ Get the start and end date for a budget """

    # Get budget object
    budget = Budget.query.filter_by(category_id=category_id, budget_userid=id).all()

    if len(budget) > 0:
        start_date = budget[0].budget_start_date
        end_date = budget[0].budget_end_date
    else:
        start_date = datetime.now()
        end_date = start_date

    # Return start and end dates
    return start_date, end_date


def budget_totals(category_id, id, total_price):
    """ Calculate budget minus expenditures made """

    # This is the expenditure object
    expenditure_budget = Budget.query.filter_by(category_id=category_id, budget_userid=id).first()

    # Initializes the budget at 0
    expenditure_budget_minus_expenses = 0

    # If there is a budget, this subtracts the total expenses from it, or
    # returns a statement about the user not inputting a budget yet
    if expenditure_budget is not None:
        budget_total = expenditure_budget.budget
        expenditure_budget_minus_expenses = float(budget_total) - float(total_price)

    else:
        expenditure_budget_minus_expenses = 0

    return expenditure_budget_minus_expenses


def get_budget_per_category(category_id, id):
    """ Gets budget for particular category """

    # Query the database for budgets associated with the user at hand
    budget = Budget.query.filter_by(budget_userid=id, category_id=category_id).all()

    # If a budget exists, return it, otherwise return 0
    if len(budget) > 0:
        budget = budget[0].budget
    else:
        budget = 0

    return budget


def get_total_for_category(cat, lst):
    """ Gets the total amount per category """

    # Set total to 0
    total = 0
    queries = lst

    # Extract expenditures by id and add the price to the total
    for query in queries:
        if query.category_id == cat:
            total += query.price

    return total


def get_progress(cat_minus_expenses, budget):
    """ Get the progress bar percentage """

    # Get perentage for progress bar and account for possible divide by 0 error
    try:
        progress = (float(cat_minus_expenses)/float(budget))
    except ZeroDivisionError:
        progress = 0

    # Multiply above total by 100 for a percentage between 1 and 100
    cat_progress = str(progress * 100)

    return cat_progress
