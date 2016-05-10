from jinja2 import StrictUndefined

from flask import Flask, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, connect_to_db

app = Flask(__name__)

app.secret_key = "CATS123"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage """

    return render_template("homepage.html", user_session_info=session)


@app.route('/dashboard/<int:id>')
def dashboard():
    """ This is the user dashboard """

    # if the user is logged into the session, check the user's id
    # and gather information about the user based on this
    if id in session:
        user = User.query.filter_by(id=id).first()

    return render_template("dashboard.html",
                            email=user.email,
                            password=user.password,
                            username=user.username)


@app.route('/login')
def login():



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
