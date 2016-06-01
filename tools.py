from model import Expenditure, Budget


def expenditure_function(category_id, id):
    """ Calculate the total amount and avg spent in one particular category """

    # List of expenditure objects
    expenditures = Expenditure.query.filter_by(category_id=category_id, expenditure_userid=id).all()

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


# The following functon gets the budget minus expenditures
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
        expenditure_budget_minus_expenses = "You haven't added a budget yet"

    return expenditure_budget_minus_expenses


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


def date_query(past, today):
    """ Get a list of expenditure objects for the past 30 days """

    # Query the database for expenditures between 2 date parameters
    query = Expenditure.query.filter(Expenditure.date_of_expenditure.between(past, today)).all()

    return query
