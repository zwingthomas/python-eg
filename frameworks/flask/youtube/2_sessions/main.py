# Acknowledgements
# Tech with Tim - video series
# Flask Tutorial #5 - Sessions
# https://www.youtube.com/watch?v=iIhAfX4iek0&ab_channel=TechWithTim
# Flask Tutorial #6 - Message Flashing
# https://www.youtube.com/watch?v=qbnqNWXf_tU&ab_channel=TechWithTim
# Flask Tutorial #7 - Using SQLAlchemy Database
# https://www.youtube.com/watch?v=uZnp21fu8TQ&ab_channel=TechWithTim

"""

Chapter 5
Now let's talk about sessions. We would need to login again and again
and again everytime we want to see the user's name. We would also have
to set up parameters and everything in order to just pass around the 
user name. This is where sessions come in. Sessions are great because
sessions are temporary. They're stored on the webserver. And they're
there for quick access for while the user is currently on the website.
It will store information about what the user is doing at a given time
and how they move around the website.

When you want to flash a message. You are passing information from 
one page to the next page. An example would be if you were to login,
you flash "logged in successful". Or if you logout "logout successful".

"""


from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
# NEED to define a secret key in order to use sessions
# it should be a very secure hash
app.secret_key = "Helloworld"
app.permanent_session_lifetime = timedelta(days=5)


@app.route("/")
def home():
    # Can add in-line html when returning from a function
    return render_template("index.html",
                           content=["tim", "joe", "bill"],
                           r="2")


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
        flash("You are now logged in.")
        return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            flash("Already logged in.")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    flash("You are not logged in.")
    return redirect(url_for("login"))


# When a user logs out, remove all session data from the server
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logout successful", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)  # debug means you don't need to rerun on changes
