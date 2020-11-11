"""Import packages and modules."""
import os
import requests
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_login import login_user, logout_user, current_user
from datetime import date, datetime
from pprint import PrettyPrinter
from events_app.main.utils import get_holiday_data
from events_app.models import Event, Guest, User

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint("main", __name__)

##########################################
#            App setup                   #
##########################################

# Define global variables (stored here for now)

# This initializes our PrettyPrinter object:

pp = PrettyPrinter(indent=4)

today = date.today()
# Now, let's just get the month as a number:
month = today.strftime("%m")
# Now, let's get the current year:
year = today.strftime("%Y")
# I also want to know the name of the month for later:
month_name = today.strftime("%B")


##########################################
#           Main Routes                  #
##########################################


@main.route("/")
def homepage():
    """
    Return template for home.

    Show upcoming events to users!
    """
    events = Event.query.all()
    return render_template("index.html", events=events)


@main.route("/add-event", methods=["POST"])
def add_event():
    """Add event to Event table."""
    try:
        new_event_title = request.form.get("title")
        new_event_description = request.form.get("description")
        new_event_date = datetime.strptime(
            request.form.get("date"), "%m-%d-%Y"
        )
        new_event_time = datetime.strptime(request.form.get("time"), "%H:%M")

        event = Event(
            title=new_event_title,
            description=new_event_description,
            date=new_event_date,
            time=new_event_time,
            guests=[],
        )

        db.session.add(event)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    except ValueError:
        return redirect(url_for("main.homepage"))


@main.route("/delete-event/<event_id>", methods=["POST"])
def delete_event(event_id):
    """
    Delete event.

    Delete event after the date it occurs automatically.
    """
    event = Event.query.filter_by(id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("main.homepage"))


@main.route("/edit-event/<event_id>", methods=["POST"])
def edit_event(event_id):
    """Edit events."""
    event = Event.query.filter_by(id=event_id).first()

    new_event_title = request.form.get("title")
    new_event_description = request.form.get("description")
    new_event_date = datetime.strptime(request.form.get("date"), "%m-%d-%Y")
    new_event_time = datetime.strptime(request.form.get("time"), "%H:%M")

    event.title = new_event_title
    event.description = new_event_description
    event.date = new_event_date
    event.time = new_event_time

    db.session.commit()
    return redirect(url_for("main.homepage"))


@main.route("/holidays")
def about_page():
    """Show user event information."""
    url = "https://calendarific.com/api/v2/holidays"

    params = {
        "api_key": os.getenv("API_KEY"),
        "country": "US",
        "year": year,
        "month": month,
    }

    result_json = requests.get(url, params=params).json()
    # You can use pp.pprint() to print out your result -
    # This will help you know how to access different items if you get stuck
    # pp.pprint(result_json)

    # Call get_holiday_data to return our list item

    holidays = get_holiday_data(result_json)

    context = {"holidays": holidays, "month": month_name}

    return render_template("about.html", **context)


@main.route("/guests", methods=["GET", "POST"])
def show_guests():
    """
    Show guests that have RSVP'd.

    Add guests to RSVP list if method is POST.
    """
    events = Event.query.all()
    if request.method == "GET":
        return render_template("guests.html", events=events)
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        plus_one = request.form.get("plus-one")
        phone = request.form.get("phone")
        event_id = request.form.get("event_id")

        event = Event.query.filter_by(id=event_id).first()

        guest = Guest(
            name=name,
            email=email,
            plus_one=plus_one,
            phone=phone,
            events_attending=[],
        )

        event.guests.append(guest)

        print(f"Event guests: {event.guests}")

        db.session.add(guest)
        db.session.commit()

        return render_template("guests.html", events=events)


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    events = Event.query.all()
    return render_template("rsvp.html", events=events)


##########################################
#           User Routes                  #
##########################################


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in user.

    For user that we already have in db.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
        elif password != user.password:
            flash("Incorrect password")
        else:
            flash("User not found. Do you need to sign up?")
    return render_template("login.html")


@main.route("/register", methods=["GET", "POST"])
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
        if password == confirm_pass:
            user = User(
                name=name, username=username, email=email, password=password
            )
            db.session.add(user)
            db.session.commit()
            flash("Thank you for signing up! You can now log in.")
            return redirect(url_for("main.login"))
        flash("Please ensure that your passwords match.")
        return redirect(url_for("main.register"))
    return render_template("register.html")


@main.route("/user")
def user():
    """
    Display user info page.

    Provide way to log out.
    """
    pass


@main.route("/logout")
def logout():
    """Log out user."""
    pass


@main.route("/admin")
def admin():
    """
    Access to edit, delete and add events.

    Special access required for this route.
    """
    pass
