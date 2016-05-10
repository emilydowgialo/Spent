from jinja2 import StrictUndefined

from flask import Flask, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db

app = Flask(__name__)

app.secret_key = "CATS123"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("login.html", user_session_info=session)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
