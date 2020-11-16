"""Package & Module import."""
import os
import requests
from flask import render_template, Blueprint
from events_app.holidays.utils import (
    get_holiday_data,
    month,
    year,
    month_name,
)

holiday = Blueprint("holiday", __name__)


@holiday.route("/holidays")
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
