from typing import List, Optional, Tuple, Union

from datetime import (
    date,
    datetime,
    timedelta,
)

import pandas as pd
from randomtimestamp import randomtimestamp

from pyutils.core.exceptions import raise_exception_if_invalid_option


DATE_STRING_FORMAT = "%Y-%m-%d" # Eg: "2020-03-19"
DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S" # Eg: "2020-03-19 17:45:08"
TIMESTAMP_INTEGER_FORMAT = "%Y%m%d%H%M%S" # Will be converted to an integer after parsing


def get_current_timestamp_as_integer() -> int:
    """Returns current timestamp as an integer (Format: yyyymmddhhmmss)"""
    dt_obj = datetime.now()
    ts_now = dt_obj.strftime(TIMESTAMP_INTEGER_FORMAT)
    return int(ts_now)


def get_random_timestamp_as_integer() -> int:
    """Returns random timestamp as an integer (Format: yyyymmddhhmmss)"""
    ts_random = randomtimestamp(
        start_year=1900,
        end_year=datetime.now().year - 1,
        pattern=TIMESTAMP_INTEGER_FORMAT,
    )
    return int(ts_random)


def get_random_timestamp(
        start_year: Optional[int] = 1800,
        end_year: Optional[int] = 2200,
    ) -> datetime:
    return datetime.strptime(randomtimestamp(start_year=start_year, end_year=end_year), "%d-%m-%Y %H:%M:%S")


def period_to_datetime(period_obj: pd._libs.tslibs.period.Period) -> datetime:
    """Converts Pandas period object to datetime object"""
    dt_obj = datetime(
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
    ) -> datetime:
    """
    Parameters:
        - date_string (str): Date string of format "yyyy-mm-dd"
        - hour (int): Ranges from 0 to 23, indicating hour of the day
        - minute (int): Ranges from 0 to 59, indicating minute of the hour
        - second (int): Ranges from 0 to 59, indicating second of the minute
    """
    year, month, day = date_string.split('-')
    dt_obj = datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=hour,
        minute=minute,
        second=second,
    )
    return dt_obj


def to_date_string(dt_obj: datetime) -> str:
    """Converts datetime object to date string of format 'yyyy-mm-dd'"""
    date_string = dt_obj.strftime(DATE_STRING_FORMAT)
    return date_string


def to_datetime_string(dt_obj: datetime) -> str:
    """Converts datetime object to datetime string of format 'yyyy-mm-dd hh:mm:ss'"""
    datetime_string = dt_obj.strftime(DATETIME_STRING_FORMAT)
    return datetime_string


def parse_date_string(date_string: str) -> datetime:
    """
    Parses date string of format 'yyyy-mm-dd' into datetime object.
    >>> parse_date_string(date_string="2020-03-28")
    """
    dt_obj = datetime.strptime(date_string, DATE_STRING_FORMAT)
    return dt_obj


def parse_datetime_string(datetime_string: str) -> datetime:
    """
    Parses datetime string of format 'yyyy-mm-dd hh:mm:ss' into datetime object.
    Note: The 'hour' in the `datetime_string` must be of 24 hour format (from 0-23).
    >>> parse_datetime_string(datetime_string="2020-03-28 17:53:04")
    """
    dt_obj = datetime.strptime(datetime_string, DATETIME_STRING_FORMAT)
    return dt_obj


def ist_to_utc(dt_obj: datetime) -> datetime:
    """Subtracts 5 hours and 30 minutes from datetime object"""
    return dt_obj - timedelta(hours=5, minutes=30)


def utc_to_ist(dt_obj: datetime) -> datetime:
    """Adds 5 hours and 30 minutes to datetime object"""
    return dt_obj + timedelta(hours=5, minutes=30)


def convert_to_naive_timezone(dt_obj: datetime) -> datetime:
    """Converts datetime object to datetime object with a naive timezone"""
    dt_obj_naive_tz = dt_obj.replace(tzinfo=None)
    return dt_obj_naive_tz



class DateWiseBucketer:
    """
    Class that provides functionality to get date-wise buckets of date-ranges.
    
    >>> dwb = DateWiseBucketer(
            date_string="2016-05-25",
            num_days_per_bucket=7,
            num_buckets=10,
        )
    >>> dwb.get_buckets(backward=False, as_type='string')
    >>> dwb.get_buckets(backward=True, as_type='string')
    """
    
    def __init__(
            self,
            date_string: str,
            num_days_per_bucket: int,
            num_buckets: int,
        ) -> None:
        """
        Parameters:
            - date_string (str): Date-string of format 'yyyy-mm-dd'
            - num_days_per_bucket (int): Number of days per bucket (must be > 0)
            - num_buckets (int): Number of buckets (must be > 0)
        """
        self.date_string = date_string
        self.num_days_per_bucket = num_days_per_bucket
        self.num_buckets = num_buckets
    
    def __str__(self) -> str:
        return f"DateWiseBucketer(date_string='{self.date_string}', num_days_per_bucket={self.num_days_per_bucket}, num_buckets={self.num_buckets})"
    
    def get_buckets(
            self,
            backward: Optional[bool] = False,
            as_type: Optional[str] = 'string',
        ) -> Union[List[Tuple[datetime, datetime]], List[Tuple[date, date]], List[Tuple[str, str]]]:
        """
        Returns list of tuples of (start_date, end_date) buckets. They will always be in ascending order.
        Options for `as_type` are: ['date', 'datetime', 'string']. Default: 'string'.
        """
        raise_exception_if_invalid_option(
            option_name='as_type',
            option_value=as_type,
            valid_option_values=['date', 'datetime', 'string'],
        )
        freq = f"-{self.num_days_per_bucket}D" if backward else f"{self.num_days_per_bucket}D"
        period_objs = pd.date_range(start=self.date_string, freq=freq, periods=self.num_buckets)
        dt_bucket_start_dates = sorted(list(map(period_to_datetime, period_objs)), reverse=False)
        if backward:
            buckets = list(map(lambda dt_obj: (dt_obj - timedelta(days=self.num_days_per_bucket - 1), dt_obj), dt_bucket_start_dates))
        else:
            buckets = list(map(lambda dt_obj: (dt_obj, dt_obj + timedelta(days=self.num_days_per_bucket - 1)), dt_bucket_start_dates))
        if as_type == 'date':
            buckets = list(map(lambda bucket: (bucket[0].date(), bucket[1].date()), buckets))
        elif as_type == 'string':
            buckets = list(map(lambda bucket: (to_date_string(bucket[0]), to_date_string(bucket[1])), buckets))
        return buckets



class MonthWiseBucketer:
    """
    Class that provides functionality to get month-wise buckets of date-ranges.
    
    >>> mwb = MonthWiseBucketer(
            year=2016,
            month=5,
            num_buckets=10,
        )
    >>> mwb.get_buckets(backward=False, as_type='string')
    >>> mwb.get_buckets(backward=True, as_type='string')
    """

    def __init__(
            self,
            year: int,
            month: int,
            num_buckets: int,
        ) -> None:
        """
        Parameters:
            - year (int): Year as integer
            - month (int): Month as integer (Range: 1-12)
            - num_buckets (int): Number of buckets (must be > 0)
        """
        self.year = year
        self.month = month
        self.num_buckets = num_buckets
    
    def __str__(self) -> str:
        return f"MonthWiseBucketer(year={self.year}, month={self.month}, num_buckets={self.num_buckets})"
    
    def get_buckets(
            self,
            backward: Optional[bool] = False,
            as_type: Optional[str] = 'string',
        ) -> Union[List[Tuple[datetime, datetime]], List[Tuple[date, date]], List[Tuple[str, str]]]:
        """
        Returns list of tuples of (start_date, end_date) buckets. They will always be in ascending order.
        Options for `as_type` are: ['date', 'datetime', 'string']. Default: 'string'.
        """
        raise_exception_if_invalid_option(
            option_name='as_type',
            option_value=as_type,
            valid_option_values=['date', 'datetime', 'string'],
        )
        period_objs = pd.date_range(
            start=datetime(year=self.year, month=self.month, day=1).strftime(DATE_STRING_FORMAT),
            freq="-1M" if backward else "1M",
            periods=self.num_buckets,
        )
        dt_bucket_end_dates = sorted(list(map(period_to_datetime, period_objs)), reverse=False)
        buckets = list(map(lambda dt_obj: (dt_obj.replace(day=1), dt_obj), dt_bucket_end_dates))
        if as_type == 'date':
            buckets = list(map(lambda bucket: (bucket[0].date(), bucket[1].date()), buckets))
        elif as_type == 'string':
            buckets = list(map(lambda bucket: (to_date_string(bucket[0]), to_date_string(bucket[1])), buckets))
        return buckets