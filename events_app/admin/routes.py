"""Package & module import."""
from datetime import datetime
from flask import render_template, redirect, url_for, Blueprint, request
from events_app import db
from events_app.models import Event
from events_app.admin.utils import admin_required

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@admin_required
def admin_page():
    """
    Access to edit, delete and add events.

    Special access required for this route.
    """
    events = Event.query.all()
    return render_template("admin.html", events=events)


@admin.route("/admin/add-event", methods=["POST"])
@admin_required
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


@admin.route("/admin/edit-event/<event_id>", methods=["POST"])
@admin_required
def admin_edit(event_id):
    """Allow admin to edit events."""
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


@admin.route("/admin/delete-event/<event_id>", methods=["POST"])
@admin_required
def admin_delete(event_id):
    """
    Delete event.

    Stretch: Delete event after the date it occurs automatically.
    """
    event = Event.query.filter_by(id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("main.homepage"))
