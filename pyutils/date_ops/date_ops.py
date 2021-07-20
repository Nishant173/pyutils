import datetime
from datetime import timedelta

import pandas as pd
from randomtimestamp import randomtimestamp

DATE_STRING_FORMAT = "%Y-%m-%d" # Eg: "2020-03-19"
DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S" # Eg: "2020-03-19 17:45:08"
TIMESTAMP_INTEGER_FORMAT = "%Y%m%d%H%M%S" # Will be converted to an integer after parsing


def get_current_timestamp_as_integer() -> int:
    dt_obj = datetime.datetime.now()
    ts_now = dt_obj.strftime(TIMESTAMP_INTEGER_FORMAT)
    return int(ts_now)


def get_random_timestamp_as_integer() -> int:
    ts_random = randomtimestamp(
        start_year=1900,
        end_year=datetime.datetime.now().year - 1,
        pattern=TIMESTAMP_INTEGER_FORMAT,
    )
    return int(ts_random)


def period_to_datetime(period_obj: pd._libs.tslibs.period.Period) -> datetime.datetime:
    """Converts Pandas period object to datetime object"""
    dt_obj = datetime.datetime(
        year=period_obj.year,
        month=period_obj.month,
        day=period_obj.day,
        hour=period_obj.hour,
        minute=period_obj.minute,
        second=period_obj.second,
    )
    return dt_obj


def convert_to_datetime(
        date_string: str,
        hour: int,
        minute: int,
        second: int,
    ) -> datetime.datetime:
    """
    Parameters:
        - date_string (str): Date string of format "yyyy-mm-dd"
        - hour (int): Ranges from 0 to 23, indicating hour of the day
        - minute (int): Ranges from 0 to 59, indicating minute of the hour
        - second (int): Ranges from 0 to 59, indicating second of the minute
    """
    year, month, day = date_string.split('-')
    dt_obj = datetime.datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=hour,
        minute=minute,
        second=second,
    )
    return dt_obj


def to_date_string(dt_obj: datetime.datetime) -> str:
    """Converts datetime object to date string of format 'yyyy-mm-dd'"""
    date_string = dt_obj.strftime(DATE_STRING_FORMAT)
    return date_string


def to_datetime_string(dt_obj: datetime.datetime) -> str:
    """Converts datetime object to datetime string of format 'yyyy-mm-dd hh:mm:ss'"""
    datetime_string = dt_obj.strftime(DATETIME_STRING_FORMAT)
    return datetime_string


def parse_date_string(date_string: str) -> datetime.datetime:
    """
    Parses date string of format 'yyyy-mm-dd' into datetime object.
    >>> parse_date_string(date_string="2020-03-28")
    """
    dt_obj = datetime.datetime.strptime(date_string, DATE_STRING_FORMAT)
    return dt_obj


def parse_datetime_string(datetime_string: str) -> datetime.datetime:
    """
    Parses datetime string of format 'yyyy-mm-dd hh:mm:ss' into datetime object.
    Note: The 'hour' in the `datetime_string` must be of 24 hour format (from 0-23).
    >>> parse_datetime_string(datetime_string="2020-03-28 17:53:04")
    """
    dt_obj = datetime.datetime.strptime(datetime_string, DATETIME_STRING_FORMAT)
    return dt_obj