"""Create database models to represent tables."""
from events_app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import backref
from passlib.hash import sha256_crypt

# Set user loader for Flask-Login


@login_manager.user_loader
def load_user(id):
    """Define user callback for user_loader function."""
    return User.query.get(id)


########################################################################
#                   #db.Model classes                                  #
########################################################################


class User(UserMixin, db.Model):
    """
    Define User class for Flask-Login.

    We also use this to persist our users in our database.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def set_is_admin(self):
        """Set is_admin to true under certain circumstances."""
        if self.email == "sid@sid.com":
            self.is_admin = True

    def set_password(self, password):
        """Return new user from User class."""
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        """Verify hashed password and inputted password."""
        return sha256_crypt.verify(password, self.password)


class Guest(db.Model):
    """Create Guest model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    plus_one = db.Column(db.String(55), nullable=True)
    phone = db.Column(db.String(12), nullable=False)
    events_attending = db.relationship("Event", secondary="guest_event_link")

    def __repr__(self):
        """Define how we want this to look when printed."""
        return self.name


class Event(db.Model):
    """Create Event model."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90), nullable=False)
    description = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    guests = db.relationship("Guest", secondary="guest_event_link")

    def __repr__(self):
        """Define how we want this to look when printed."""
        return self.title, self.description


class GuestEventLink(db.Model):
    """Joining table for guests & events."""

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship(
        "Event", backref=backref("link", cascade="all, delete-orphan")
    )
    guest = db.relationship(
        "Guest", backref=backref("link", cascade="all, delete-orphan")
    )
