
import pytz
from datetime import datetime, timedelta

def is_less_than_x_hours_ago(date_str, hours: int = 24):
    # Define the date format
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    
    # Parse the date string into a datetime object
    parsed_date = datetime.strptime(date_str, date_format)
    
    # Get the current date and time in UTC
    current_date = datetime.now(pytz.utc)
    
    # Calculate the difference
    time_difference = current_date - parsed_date
    
    # Check if the difference is less than 48 hours
    return time_difference < timedelta(hours=hours)
