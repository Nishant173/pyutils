import datetime

import pandas as pd
from randomtimestamp import randomtimestamp


def get_current_timestamp() -> int:
    dt_obj = datetime.datetime.now()
    ts_now = dt_obj.strftime("%Y%m%d%H%M%S")
    return int(ts_now)


def get_random_timestamp() -> int:
    ts_random = randomtimestamp(
        start_year=2000,
        end_year=2020,
        pattern="%Y%m%d%H%M%S",
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