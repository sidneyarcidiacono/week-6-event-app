"""Import packages and modules."""
from flask import (
    Blueprint,
    request,
    render_template,
)
from events_app.models import Event, Guest
from events_app import db

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    """
    Return template for home.

    Show upcoming events to users!
    """
    events = Event.query.all()
    return render_template("index.html", events=events)


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

        db.session.add(guest)
        db.session.commit()

        return render_template("guests.html", events=events)


@main.route("/rsvp")
def rsvp_guest():
    """Show form for guests to RSVP for events."""
    events = Event.query.all()
    return render_template("rsvp.html", events=events)
