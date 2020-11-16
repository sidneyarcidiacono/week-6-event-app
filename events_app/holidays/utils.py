"""Helper functions for holidays."""
from datetime import date
from pprint import PrettyPrinter

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
