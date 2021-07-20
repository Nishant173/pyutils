import datetime
from datetime import timedelta


def ist_to_utc(dt_obj: datetime.datetime) -> datetime.datetime:
    return dt_obj - timedelta(hours=5, minutes=30)


def utc_to_ist(dt_obj: datetime.datetime) -> datetime.datetime:
    return dt_obj + timedelta(hours=5, minutes=30)


def convert_to_naive_timezone(dt_obj: datetime.datetime) -> datetime.datetime:
    dt_obj_naive_tz = dt_obj.replace(tzinfo=None)
    return dt_obj_naive_tz