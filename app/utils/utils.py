
import pytz
from time import sleep
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

def check_time_and_run(target_hour, target_minute):
    while True:
        # Get the current time
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Check if the current time matches the target time
        if current_hour == target_hour and current_minute == target_minute:
            run_summarization()
            # Wait for 60 seconds to avoid running multiple times within the same minute
            sleep(60)
        else:
            # Sleep for a short time to avoid busy waiting
            sleep(30)