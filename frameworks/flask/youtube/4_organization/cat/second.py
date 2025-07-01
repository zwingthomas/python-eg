from flask import Blueprint, render_template

# Always name this after the file, the second import will always be
# __name__ pretty much. You should also link up your static and
# templates folders.
second = Blueprint("second",
                   __name__,
                   static_folder="static",
                   template_folder="template")


@second.route("/home")
@second.route("/")
def home():
    return render_template("home.html")
