from typing import Any, Dict, List
import random

import numpy as np

from pyutils.core.type_annotations import (
    Number,
    NumberOrString,
)


def is_none_or_nan(value: Any) -> bool:
    """Returns True if value given is Python's native None or Numpy's NaN. Otherwise returns False"""
    if value is None:
        return True
    if isinstance(value, float):
        if np.isnan(value):
            return True
    return False


def get_timetaken_dictionary(num_seconds: Number) -> Dict[str, Number]:
    """Returns dictionary having the following keys: ['h', 'm', 's'], denoting the time elapsed based on `num_seconds` given"""
    days, hrs, mins, secs = 0, 0, 0, 0
    decimal_after_secs = None
    if int(num_seconds) == num_seconds:
        num_seconds = int(num_seconds)
    else:
        decimal_after_secs = num_seconds - np.floor(num_seconds)
        num_seconds = int(np.floor(num_seconds))
    if num_seconds < 60:
        secs = num_seconds
    elif 60 <= num_seconds < 3600:
        mins, secs = divmod(num_seconds, 60)
    elif 3600 <= num_seconds < 3600 * 24:
        hrs, secs_remainder = divmod(num_seconds, 3600)
        mins, secs = divmod(secs_remainder, 60)
    else:
        days, secs_remainder = divmod(num_seconds, 3600 * 24)
        hrs, secs_remainder = divmod(secs_remainder, 3600)
        mins, secs = divmod(secs_remainder, 60)
    dictionary_timetaken = {
        "d": days,
        "h": hrs,
        "m": mins,
        "s": round(secs + decimal_after_secs, 2) if decimal_after_secs else secs,
    }
    dictionary_timetaken = {key: value for key, value in dictionary_timetaken.items() if value > 0}
    return dictionary_timetaken


def get_timetaken_fstring(num_seconds: Number) -> str:
    """Returns string denoting the time elapsed based on `num_seconds` given"""
    dict_timetaken = get_timetaken_dictionary(num_seconds=num_seconds)
    timetaken_components = [f"{value}{unit}" for unit, value in dict_timetaken.items()]
    return " ".join(timetaken_components).strip()


def get_random_choice_except(
        choices: List[NumberOrString],
        exception: NumberOrString,
    ) -> NumberOrString:
    """Gets random choice from an iterable, given an exception"""
    if exception not in choices:
        raise ValueError("The `exception` is not available in the given `choices`")
    choices_available = list(set(choices).difference(set([exception])))
    if not choices_available:
        raise ValueError("No choices available")
    return random.choice(choices_available)


def round_off_as_string(number: Number, round_by: int) -> str:
    """
    Rounds off the given `number` to `round_by` decimal places, and type casts
    it to a string (to retain the exact number of decimal places desired).
    """
    if round_by < 0:
        raise ValueError("The `round_by` parameter must be >= 0")
    if round_by == 0:
        return str(round(number))
    number_stringified = str(round(number, round_by))
    decimal_places_filled = len(number_stringified.split('.')[-1])
    decimal_places_to_fill = round_by - decimal_places_filled
    for _ in range(decimal_places_to_fill):
        number_stringified += '0'
    return number_stringified


def commafy_number(number: Number) -> str:
    """
    Adds commas to number for better readability.
    >>> commafy_number(number=1738183090) # Returns "1,738,183,090"
    >>> commafy_number(number=1738183090.90406) # Returns "1,738,183,090.90406"
    """
    if int(number) == number:
        return format(int(number), ",d")
    return format(number, ",f")


def integerify_if_possible(number: Number) -> Number:
    """Converts whole numbers represented as floats to integers"""
    if int(number) == number:
        return int(number)
    return number


def string_to_int_or_float(value: str) -> Number:
    """Converts stringified number to either int or float"""
    number = float(value)
    number = integerify_if_possible(number=number)
    return number


def stringify_list_of_nums(array: List[Number]) -> str:
    """Converts list of ints/floats to comma separated string of the same"""
    return ",".join(list(map(str, array)))


def listify_string_of_nums(string: str) -> List[Number]:
    """Converts string of comma separated ints/floats to list of numbers"""
    numbers = string.split(',')
    numbers = list(map(string_to_int_or_float, numbers))
    return numbers


def get_max_of_abs_values(array: List[Number]) -> Number:
    """Finds maximum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return max(array_abs)


def get_min_of_abs_values(array: List[Number]) -> Number:
    """Finds minimum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return min(array_abs)


def has_negative_number(array: List[Number]) -> bool:
    for number in array:
        if number < 0:
            return True
    return False


def has_positive_number(array: List[Number]) -> bool:
    for number in array:
        if number > 0:
            return True
    return False


def get_indices_for_partitioning(
        length_of_iterable: int,
        num_partitions: int,
    ) -> List[int]:
    """Returns list of indices to partition an iterable, given the number of partitions"""
    if num_partitions == 0:
        raise ValueError("Number of partitions cannot be 0")
    indices_for_partitioning = [0]
    min_length_per_partition = int(np.floor(length_of_iterable / num_partitions))
    num_residuals = int(length_of_iterable % num_partitions)
    while num_residuals > 0:
        latest_idx = indices_for_partitioning[-1]
        length_of_partition = min_length_per_partition + 1
        num_residuals -= 1
        indices_for_partitioning.append(latest_idx + length_of_partition)
    while len(indices_for_partitioning) != num_partitions + 1:
        latest_idx = indices_for_partitioning[-1]
        indices_for_partitioning.append(latest_idx + min_length_per_partition)
    return indices_for_partitioning