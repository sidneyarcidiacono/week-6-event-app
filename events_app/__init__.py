"""Import packages and modules for initializing our app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from events_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)


# TODO: Use the instructions in your assignment
# to initialize your database taking our app as its parameter.

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "main.login"

from events_app.main.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()
