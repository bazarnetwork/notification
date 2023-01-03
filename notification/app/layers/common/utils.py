import datetime
import random
import string
from .constants import timestamp_format

def get_random_string(length):
        result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
        return f"{result_str}"

def get_current_datetime():
        now = datetime.datetime.now() 
        date_time = now.strftime(timestamp_format)
        return f"{date_time}"