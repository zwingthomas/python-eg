# Acknowledgements____
# Tech with Tim
# Flask Tutorial #9 - Static Files (Custom CSS, Images & Javascript)
# https://www.youtube.com/watch?v=tXpFERibRaU&ab_channel=TechWithTim
# Flask Tutorial #10 - Blueprints & Using Multiple Python Files
# https://www.youtube.com/watch?v=WteIH6J9v64&ab_channel=TechWithTim

"""
In Flask there is kind of a weird way of loading in custom CSS and
images. We call these static files. All these static files go into
the static/ directory. The main thing to know is that the folder
structure is very important. It must be named "static".

File organization - multiple python files____
main.py sets up blueprint files. Blueprint paths take precedent over
the main.py file routes if there are collisions. Use url_prefix to
avoid collisions! This then passes the rest of the url to that path.

You can also use different templates and different static folders for
each blueprint! This allows you to have different apps in one 
webpage!
"""

from flask import Flask, render_template
from cat.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/cat")


@app.route("/")
def home():
    return "<h1>Test</h1>"


if __name__ == "__main__":
    app.run(debug=True)
