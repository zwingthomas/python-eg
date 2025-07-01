# Acknowledgements
# Tech with Tim - video series
# Flask Tutorial #1 - How to Make Websites with Python
# https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&ab_channel=TechWithTim
# Flask Tutorial #2 - HTML Templates
# https://www.youtube.com/watch?v=xIgPMguqyws&ab_channel=TechWithTim
# Flask Tutorial #3 - Adding Bootstrap and Template Inheritance
# https://www.youtube.com/watch?v=4nzI4RKwb5I&ab_channel=TechWithTim
# Flask Tutorial #4 - HTTP Methods (GET/POST) & Retrieving Form Data
# https://www.youtube.com/watch?v=9MHYHgh4jYc&ab_channel=TechWithTim


"""
Flask is a micro-framework. Compared to Django things are a lot more
simple and make a lot more sense. However, it does not include a lot
of the nice things included in Django like user authentication. Still
it allows you to build a full website very quickly.

GET/POST
These are ways of sending information to our server or to our client.
We go through how we'd pass through some password data or some name
data from a form to the backend of the site and we can do some more
advanced stuff with that.

POST - usually secure, will not be stored on the server unless in db
GET - usually we don't care if this is secure or not

Chapter 5
Now let's talk about sessions. We would need to login again and again
and again everytime we want to see the user's name. We would also have
to set up parameters and everything in order to just pass around the 
user name. This is where sessions come in. Sessions are great because
sessions are temporary. They're stored on the webserver. And they're
there for quick access for while the user is currently on the website.
It will store information about what the user is doing at a given time
and how they move around the website.

"""


from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    # Can add in-line html when returning from a function
    return render_template("index.html",
                           content=["tim", "joe", "bill"],
                           r="2")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


# @app.route("/<name>")
# def user(name):
#     # <name> means it will pass it as a value to the parameter
#     return f"Hello {name}!"


@app.route("/test")
def new(name):
    return render_template("new.html")


@app.route("/admin")
def admin():
    # Pass in the function name, not the route
    return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    app.run(debug=True)  # debug means you don't need to rerun on changes
