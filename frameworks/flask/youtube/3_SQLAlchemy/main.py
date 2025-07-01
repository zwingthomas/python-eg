# Acknowledgements
# Tech with Tim - video series
# Flask Tutorial #5 - Sessions
# https://www.youtube.com/watch?v=iIhAfX4iek0&ab_channel=TechWithTim
# Flask Tutorial #6 - Message Flashing
# https://www.youtube.com/watch?v=qbnqNWXf_tU&ab_channel=TechWithTim
# Flask Tutorial #7 - Using SQLAlchemy Database
# https://www.youtube.com/watch?v=uZnp21fu8TQ&ab_channel=TechWithTim

"""

This section is on SQLAlchemy and persisting user data. See the
SQLAlchemy section of this repo for more information.

"""


from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# NEED to define a secret key in order to use sessions
# it should be a very secure hash
app.secret_key = "Helloworld"
app.permanent_session_lifetime = timedelta(days=5)
# Users is the table here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# Remove a warning, makes it so we're not tracking all the modifications
# to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating a database for our app
db = SQLAlchemy()
db.init_app(app)

# Now we create a model (an object) that we can use to store our data
# in and then use to store that object into our database using
# SQLAlchemy as the ORM


class users(db.Model):
    # Every object in the db needs a unique identifier
    # This can often be an id, these are denoted with unique
    # or with primary_key=True
    _id = db.Column("id", db.Integer, primary_key=True)
    # new column
    name = db.Column(db.String(100))
    # new column
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    # Can add in-line html when returning from a function
    return render_template("index.html",
                           content=["tim", "joe", "bill"],
                           r="2")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # This makes sessions permanent, so login once unless logout
        # By default your session lasts as long as you're in your
        # browser.
        session.permanent = True
        user = request.form["nm"]
        # When you close the browser the session does not persist
        session["user"] = user
        """ DATABASE SECTION """
        found_user = users.query.filter_by(name=user).first()
        # This will return and delete one object, doesn't go into
        # effect till it is committed
        # found_user = users.query.filter_by(name=user).delete()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(name=user, email=None)
            db.session.add(usr)
            # Remember rollbacks and priciples of atomicity
            db.session.commit()

        flash("You are now logged in.")
        return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            flash("Already logged in.")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            # Grab email from the html template
            email = request.form["email"]
            """ DATABASE SECTION """
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            # Remember rollbacks and priciples of atomicity
            db.session.commit()
            flash("Email was saved!")
        else:
            email = session["email"] if "email" in session else None
        return render_template("user.html", email=email)
    flash("You are not logged in.")
    return redirect(url_for("login"))


# When a user logs out, remove all session data from the server
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("Logout successful", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # debug means you don't need to rerun on changes
