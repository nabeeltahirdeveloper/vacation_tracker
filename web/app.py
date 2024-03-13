#!usr/bin/python3
"""
script to start a flask web application
"""

from models import storage, User
from flask import Flask, render_template
import uuid

app = Flask(__name__)


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()

@app.route('/home', strict_slashes=False, methods=["GET"])
def home():
    """
    home
    """
    return render_template("home.html")

@app.route("/", strict_slashes=False, methods=["GET", "POST"])
@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """
    Login
    """
    return render_template("login.html")


@app.route("/dashboard", strict_slashes=False, methods=["GET", "POST"])
def dashboard():
    """
    users
    """
    return render_template(
        "dashboard.html",
        users=storage.all(User),
        name=type(storage.all(User)),
        cache_id=uuid.uuid4()
    )


@app.route("/forgot-password", strict_slashes=False, methods=["GET", "POST"])
def forgot_password():
    """
    forgot-password
    """
    return render_template("forgot-password.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
