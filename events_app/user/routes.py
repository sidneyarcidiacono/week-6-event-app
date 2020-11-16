"""Package & module import."""
from flask import (
    render_template,
    flash,
    Blueprint,
    redirect,
    url_for,
    request,
)
from flask_login import login_user, login_required, logout_user
from events_app import db
from events_app.models import User

user = Blueprint("user", __name__)


@user.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in user.

    For user that we already have in db.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("You are now logged in.")
            return redirect(url_for("main.homepage"))
        elif user and password != user.password:
            flash("Incorrect password")
        else:
            flash("User not found. Do you need to sign up?")
    return render_template("login.html")


@user.route("/register", methods=["GET", "POST"])
def register():
    """
    Sign up user.

    For user that does not yet exist.
    """
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm-password")
        check_for_user = User.query.filter_by(email=email).all()
        if not check_for_user and password == confirm_pass:
            user = User(
                name=name, username=username, email=email, password=password
            )
            user.set_is_admin()
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Thank you for signing up! You can now log in.")
            return redirect(url_for("user.login"))
        elif check_for_user:
            flash("A user with this email already exists.")
        else:
            flash("Please ensure that your passwords match.")
            return redirect(url_for("user.register"))
    return render_template("register.html")


@user.route("/user")
@login_required
def user_page():
    """
    Display user info page.

    Provide way to log out.
    """
    return render_template("user.html")


@user.route("/logout")
@login_required
def logout():
    """Log out user."""
    logout_user()
    return redirect(url_for("main.homepage"))
