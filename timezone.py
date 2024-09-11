from datetime import datetime
import pytz


def convert_utc_to_central(utc_timestamp_str):
    timestamp_format = "%Y/%m/%d %H:%M:%S"

    utc_time = datetime.strptime(utc_timestamp_str, timestamp_format)

    # Define the UTC and Central Time zones
    utc_zone = pytz.utc
    central_zone = pytz.timezone('US/Central')

    utc_time = utc_zone.localize(utc_time)

    # Convert the datetime object to Central Time
    central_time = utc_time.astimezone(central_zone)

    return central_time.strftime(timestamp_format)
