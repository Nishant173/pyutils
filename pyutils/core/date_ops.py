from typing import List, Optional, Tuple, Union

from datetime import (
    date,
    datetime,
    timedelta,
)

import pandas as pd
from randomtimestamp import randomtimestamp

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
            is_inclusive=False,
        )
    >>> dwb.get_forward_buckets(as_strings=True)
    >>> dwb.get_backward_buckets(as_strings=True)
    """
    
    def __init__(
            self,
            date_string: str,
            num_days_per_bucket: int,
            num_buckets: int,
            is_inclusive: Optional[bool] = False,
        ) -> None:
        self.date_string = date_string
        self.num_days_per_bucket = num_days_per_bucket
        self.num_buckets = num_buckets
        self.is_inclusive = is_inclusive
    
    def __str__(self) -> str:
        return f"DateWiseBucketer(date_string='{self.date_string}', num_days_per_bucket={self.num_days_per_bucket}, num_buckets={self.num_buckets}, is_inclusive={self.is_inclusive})"
    
    def get_forward_buckets(self, as_strings: Optional[bool] = False) -> Union[List[Tuple[date, date]], List[Tuple[str, str]]]:
        """Returns list of tuples having (start_date, end_date) buckets"""
        dt_obj = parse_date_string(date_string=self.date_string)
        date_range_buckets = []
        for _ in range(self.num_buckets):
            dt_start = dt_obj
            dt_end = dt_obj + timedelta(days=self.num_days_per_bucket - 1)
            start = to_date_string(dt_obj=dt_start) if as_strings else dt_start.date()
            end = to_date_string(dt_obj=dt_end) if as_strings else dt_end.date()
            date_range_buckets.append((start, end))
            if self.is_inclusive:
                dt_obj += timedelta(days=self.num_days_per_bucket - 1)
            else:
                dt_obj += timedelta(days=self.num_days_per_bucket)
        return date_range_buckets
    
    def get_backward_buckets(self, as_strings: Optional[bool] = False) -> Union[List[Tuple[date, date]], List[Tuple[str, str]]]:
        """Returns list of tuples having (start_date, end_date) buckets"""
        dt_obj = parse_date_string(date_string=self.date_string)
        date_range_buckets = []
        for _ in range(self.num_buckets):
            dt_end = dt_obj
            dt_start = dt_obj - timedelta(days=self.num_days_per_bucket - 1)
            start = to_date_string(dt_obj=dt_start) if as_strings else dt_start.date()
            end = to_date_string(dt_obj=dt_end) if as_strings else dt_end.date()
            date_range_buckets.append((start, end))
            if self.is_inclusive:
                dt_obj -= timedelta(days=self.num_days_per_bucket - 1)
            else:
                dt_obj -= timedelta(days=self.num_days_per_bucket)
        return date_range_buckets[::-1]



class MonthWiseBucketer:
    """
    Class that provides functionality to get month-wise buckets of date-ranges.
    
    >>> mwb = MonthWiseBucketer(
            year=2016,
            month=5,
            num_buckets=10,
        )
    >>> mwb.get_forward_buckets(as_strings=True)
    >>> mwb.get_backward_buckets(as_strings=True)
    """

    def __init__(
            self,
            year: int,
            month: int,
            num_buckets: int,
        ) -> None:
        self.year = year
        self.month = month
        self.num_buckets = num_buckets
    
    def __str__(self) -> str:
        return f"MonthWiseBucketer(year={self.year}, month={self.month}, num_buckets={self.num_buckets})"
    
    def __period_obj_to_month_wise_bucket(
            self,
            period_obj: pd._libs.tslibs.period.Period,
            as_strings: bool,
        ) -> Union[Tuple[date, date], Tuple[str, str]]:
        """
        Expects Pandas period object having last date of a month.
        Returns tuple of (start_date, end_date), where the dates are the first and last dates of the month.
        """
        dt_obj = period_to_datetime(period_obj=period_obj)
        start, end = dt_obj.replace(day=1).date(), dt_obj.date()
        if as_strings:
            start, end = start.strftime(DATE_STRING_FORMAT), end.strftime(DATE_STRING_FORMAT)
        return (start, end)
    
    def get_forward_buckets(self, as_strings: Optional[bool] = False) -> Union[List[Tuple[date, date]], List[Tuple[str, str]]]:
        """Returns list of tuples having month-wise (start_date, end_date) buckets"""
        start_date = datetime(year=self.year, month=self.month, day=1).strftime(DATE_STRING_FORMAT)
        period_objs = pd.date_range(start=start_date, freq='1M', periods=self.num_buckets)
        buckets = [self.__period_obj_to_month_wise_bucket(period_obj=period_obj, as_strings=as_strings) for period_obj in period_objs]
        return buckets
    
    def get_backward_buckets(self, as_strings: Optional[bool] = False) -> Union[List[Tuple[date, date]], List[Tuple[str, str]]]:
        """Returns list of tuples having month-wise (start_date, end_date) buckets"""
        start_date = datetime(year=self.year, month=self.month, day=1).strftime(DATE_STRING_FORMAT)
        period_objs = pd.date_range(start=start_date, freq='-1M', periods=self.num_buckets)
        buckets = [self.__period_obj_to_month_wise_bucket(period_obj=period_obj, as_strings=as_strings) for period_obj in period_objs]
        return buckets[::-1]