import datetime
from datetime import timedelta

import pandas as pd
from randomtimestamp import randomtimestamp

TIMESTAMP_FORMAT = "%Y%m%d%H%M%S" # Will be converted to an integer after parsing


def get_current_timestamp() -> int:
    dt_obj = datetime.datetime.now()
    ts_now = dt_obj.strftime(TIMESTAMP_FORMAT)
    return int(ts_now)


def get_random_timestamp() -> int:
    ts_random = randomtimestamp(
        start_year=1900,
        end_year=datetime.datetime.now().year - 1,
        pattern=TIMESTAMP_FORMAT,
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


def convert_to_timestamp(
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


def parse_date_string(date_string: str) -> datetime.datetime:
    """
    Parses date string of format 'yyyy-mm-dd' into datetime object.
    >>> parse_date_string(date_string="2020-03-28")
    """
    dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return dt_obj


def parse_datetime_string(datetime_string: str) -> datetime.datetime:
    """
    Parses datetime string of format 'yyyy-mm-dd hh:mm:ss' into datetime object.
    Note: The 'hour' in the `datetime_string` must be of 24 hour format (from 0-23).
    >>> parse_datetime_string(datetime_string="2020-03-28 17:53:04")
    """
    dt_obj = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return dt_obj


def utc_to_ist(dt_obj: datetime.datetime) -> datetime.datetime:
    """Adds 5 hours and 30 minutes"""
    return dt_obj + timedelta(hours=5, minutes=30)


def ist_to_utc(dt_obj: datetime.datetime) -> datetime.datetime:
    """Subtracts 5 hours and 30 minutes"""
    return dt_obj - timedelta(hours=5, minutes=30)


def convert_to_naive_timezone(dt_obj: datetime.datetime) -> datetime.datetime:
    dt_obj_converted = dt_obj.replace(tzinfo=None)
    return dt_obj_converted