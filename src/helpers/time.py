from datetime import datetime


def format_datetime_str_to_datetime(dt: str):
    formatted = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return formatted
