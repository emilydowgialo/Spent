import unittest

from server import app
from model import db, connect_to_db, User, example_data


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

        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="m"), follow_redirects=True)

        self.assertIn("Error in logging in", result.data)

    def test_signin_fail_wrong_email(self):
        """ Test for an error in logging in with the incorrect email """

        result = self.client.post("/login-form", data=dict(
            email="mu@m.com",
            password="mu"), follow_redirects=True)

        self.assertIn("Error in logging in", result.data)

    def test_signin_fail_wrong_email_and_password(self):
        """ Test for an error in logging in with the incorrect email and password """

        result = self.client.post("/login-form", data=dict(
            email="ashdgu@m.com",
            password="maskj"), follow_redirects=True)

        self.assertIn("Error in logging in", result.data)

    def test_signin_success(self):
        """ Test for successfully logging in """

        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        self.assertIn("Dashboard", result.data)

    def test_login_redirect(self):
        """ Test for successfully being redirected to the login form """

        result = self.client.post("/login-form", data=dict(
            email="mu@mu.com",
            password="mu"), follow_redirects=True)

        self.assertIn("Dashboard", result.data)


if __name__ == "__main__":
    unittest.main()
