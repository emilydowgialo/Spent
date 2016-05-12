import unittest

from server import app
from model import db, connect_to_db, User


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
        # example_data()

    def tearDown(self):
        """ Do at end of every test """

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_signup(self):
        """ Test that registering creates a new user """

        # Adding a new test user to the database
        result = self.client.post("/sign-up", data=dict(
            name="kitty",
            email="kitty@kitty.com",
            password="kitty"), follow_redirects=True)

        print
        print
        print result.data
        print
        print

        # Checking is parameter a is in b
        self.assertIn("You have successfully signed up", result.data)

        # Query the database for the newly added user
        user_test = User.query.filter_by(name="kitty").first()

        # Verify that the user email is kitty@kitty.com - it will register as True
        self.assertTrue(user_test.email == "kitty@kitty.com")


if __name__ == "__main__":
    unittest.main()
