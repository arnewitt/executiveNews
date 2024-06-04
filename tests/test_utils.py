
from datetime import datetime, timedelta
import pytz

from utils.utils import is_less_than_x_hours_ago

def test_is_less_than_x_hours_ago():
    current_time = datetime.now(pytz.utc)
    valid_time = (current_time - timedelta(hours=23)).strftime("%a, %d %b %Y %H:%M:%S %z")
    invalid_time = (current_time - timedelta(hours=25)).strftime("%a, %d %b %Y %H:%M:%S %z")

    assert is_less_than_x_hours_ago(valid_time, 24) == True
    assert is_less_than_x_hours_ago(invalid_time, 24) == False
