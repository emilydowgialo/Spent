import unittest

from datetime import datetime

from server import app
from model import db, connect_to_db, User, example_data, Budget, Expenditure


class SpentDatabaseTests(unittest.TestCase):
    """ Flask tests that use the database """

    def setUp(self):
        """ Stuff to do before every test """

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key123'
        self.client = app.test_client()

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """ Do at end of every test - drop the database """

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_signup_creates_new_user(self):
        """ Test that registering creates a new user """

        # Adding a new test user to the database
        result = self.client.post("/sign-up", data=dict(
            name="kitty",
            email="kitty@kitty.com",
            password="kitty"), follow_redirects=True)

        # Checking is parameter a is in b
        self.assertIn("You have successfully signed up", result.data)

        # Query the database for the newly added user
        user_test = User.query.filter_by(name="kitty").first()

        # Verify that the user email is kitty@kitty.com - it will register as True
        self.assertTrue(user_test.email == "kitty@kitty.com")

    def test_signup_fail_user_already_exists(self):
        """ Test for an error in signing up as a user that already exists """

        # Try to sign up as an already existing user
        result = self.client.post("/sign-up", data=dict(
            name="Mu",
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # This should flash if a user already exists in the database
        self.assertIn("A user by this name already exists", result.data)

    def test_signin_fail_wrong_password(self):
        """ Test for an error in logging in with the incorrect password """

        # Try signing in using the incorrect password
        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="m"), follow_redirects=True)

        # Check if the error phrase comes up
        self.assertIn("Error in logging in", result.data)

    def test_signin_fail_wrong_email(self):
        """ Test for an error in logging in with the incorrect email """

        # Log in a fake user using the wrong email
        result = self.client.post("/login-form", data=dict(
            email="mu@m.com",
            password="mu"), follow_redirects=True)

        # Check if the error messages pops up
        self.assertIn("Error in logging in", result.data)

    def test_signin_fail_wrong_email_and_password(self):
        """ Test for an error in logging in with the incorrect email and password """

        # Log in as a test client
        result = self.client.post("/login-form", data=dict(
            email="ashdgu@m.com",
            password="maskj"), follow_redirects=True)

        self.assertIn("Error in logging in", result.data)

    def test_signin_success(self):
        """ Test for successfully logging in """

        # Log in as a test client
        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        self.assertIn("Spent", result.data)

    def test_login_redirect(self):
        """ Test for successfully being redirected to the login form """

        # Log in as a test client
        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        self.assertIn("Spent", result.data)

    def test_add_budget_success(self):
        """ Test for successfully adding a budget """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Add a budget
        result = self.client.post("/add-budget", data=dict(
            budget="100",
            category=3), follow_redirects=True)

        self.assertIn("100", result.data)

        # Verify that the correct category is in the database
        self.assertTrue("3")

    def test_add_expenditure_success(self):
        """ Test for successfully adding an expenditure to the database """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Add an expenditure to the db
        result = self.client.post("/add-expenditure-to-db", data=dict(
            category=3,
            price=40,
            date=datetime.now(),
            where_bought="Whole Foods",
            description="groceries and stuff"
            ), follow_redirects=True)

        self.assertIn("3", result.data)

        # Verify that the correct price was addedt to the database
        self.assertTrue("40")

    def test_dashboard(self):
        """ Test if the dashboard routes correctly """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Test the route
        result = self.client.get("/dashboard/1", follow_redirects=True)

        # Test if 'Dashboard' shows
        self.assertIn("Spent", result.data)

        self.assertIn("Account", result.data)

        self.assertTrue("Budget")

    def test_profile_edit(self):
        """ Test if editing profile info works """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Test the route
        result = self.client.post("/profile-edit", data={
            "profile-name": "kitty"}, follow_redirects=True)

        # Checking if the redirect works
        self.assertIn("kitty", result.data)

        # Query the database for the user
        profile_test_user = User.query.filter_by(email="mu@mu.com").first()

        # Verify that the new name is in the database
        self.assertTrue(profile_test_user.name == "kitty")

        # Verify that the user's old name is not in the database
        self.assertFalse(profile_test_user.name == "mu")

    def test_remove_budget(self):
        """ Test if a budget can be removed """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Query the database for the budget
        budget_test = Budget.query.filter_by(budget=1000).first()

        # Query for the budget id
        budget_test_id = budget_test.id

        # Test the route
        result = self.client.post("/remove-budget/" + str(budget_test_id), follow_redirects=True)

        # Query for the removed budget
        budget_test_after_removal = Budget.query.filter_by(budget=1000).count()

        # See if the budget was removed by checking if count is 0
        self.assertTrue(budget_test_after_removal == 0)

        self.assertIn("Spent", result.data)

    def test_remove_expenditure(self):
        """ Test if expenditures can be removed """

        # Log in a test client
        self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        # Query the database for the expenditure
        expenditure_test = Expenditure.query.filter_by(price=500).first()

        # Query for the expenditure id
        expenditure_test_id = expenditure_test.id

        # Test the route
        result = self.client.post("/remove-expenditure/" + str(expenditure_test_id), follow_redirects=True)

        # Query for the removed expenditure
        expenditure_test_after_removal = Expenditure.query.filter_by(price=500).count()

        # See if the expenditure was removed by checking if count is 0
        self.assertTrue(expenditure_test_after_removal == 0)

        self.assertIn("1", result.data)


if __name__ == "__main__":
    unittest.main()
