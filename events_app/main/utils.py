"""Helper functions for app."""
from functools import wraps
from flask_login import current_user
from events_app import login_manager

# Create decorator for routes that require admin role


def admin_required(func):
    """Decorate route function to check is user isadmin."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper


def get_holiday_data(result):
    """Loop through our JSON results and get only the information we need."""
    data = []
    for holiday in result["response"]["holidays"]:
        new_holiday = {
            "name": holiday["name"],
            "description": holiday["description"],
            "date": holiday["date"]["iso"],
        }
        data.append(new_holiday)
    return data
