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