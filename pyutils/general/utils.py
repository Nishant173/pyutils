from typing import Any, Dict, List, Optional, Union
import random

import numpy as np


def get_random_choice_except(choices: List[Any], exception: Any) -> Any:
    if exception not in choices:
        raise ValueError("The `exception` is not available in the given `choices`")
    choices_available = list(set(choices).difference(set([exception])))
    if not choices_available:
        raise Exception("No choices available")
    return random.choice(choices_available)


def get_timetaken_dictionary(num_seconds: Union[int, float]) -> Dict[str, Union[int, float]]:
    hrs, mins, secs = 0, 0, 0
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
    else:
        hrs, secs_remainder = divmod(num_seconds, 3600)
        mins, secs = divmod(secs_remainder, 60)
    dictionary_timetaken = {
        "hrs": hrs,
        "mins": mins,
        "secs": secs + decimal_after_secs if decimal_after_secs else secs,
    }
    dictionary_timetaken = {key: value for key, value in dictionary_timetaken.items() if value > 0}
    return dictionary_timetaken


def get_timetaken_fstring(num_seconds: Union[int, float]) -> str:
    dict_timetaken = get_timetaken_dictionary(num_seconds=num_seconds)
    timetaken_components = [f"{value} {unit}" for unit, value in dict_timetaken.items()]
    return " ".join(timetaken_components).strip()


def commafy_number(number: Union[int, float]) -> str:
    """
    Adds commas to number for better readability.
    >>> commafy_number(number=1738183090) # Returns "1,738,183,090"
    >>> commafy_number(number=1738183090.90406) # Returns "1,738,183,090.90406"
    """
    if int(number) == number:
        return format(int(number), ",d")
    return format(number, ",f")


def generate_random_hex_code() -> str:
    """Generates random 6-digit hexadecimal code"""
    choices = '0123456789ABCDEF'
    random_hex_code = '#'
    for _ in range(6):
        random_hex_code += random.choice(choices)
    return random_hex_code


def generate_random_hex_codes(how_many: int) -> List[str]:
    """Returns list of random 6-digit hexadecimal codes"""
    random_hex_codes = [generate_random_hex_code() for _ in range(how_many)]
    return random_hex_codes


def integerify_if_possible(number: Union[int, float]) -> Union[int, float]:
    """Converts whole numbers represented as floats to integers"""
    if int(number) == number:
        return int(number)
    return number


def string_to_int_or_float(value: str) -> Union[int, float]:
    """Converts stringified number to either int or float"""
    number = float(value)
    if int(number) == number:
        number = int(number)
    return number


def stringify_list_of_nums(array: List[Union[int, float]]) -> str:
    """Converts list of ints/floats to comma separated string of the same"""
    return ",".join(list(map(str, array)))


def listify_string_of_nums(string: str) -> List[Union[int, float]]:
    """Converts string of comma separated ints/floats to list of numbers"""
    numbers = string.split(',')
    numbers = list(map(string_to_int_or_float, numbers))
    return numbers


def get_max_of_abs_values(array: List[Union[int, float]]) -> Union[int, float]:
    """Finds maximum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return max(array_abs)


def get_min_of_abs_values(array: List[Union[int, float]]) -> Union[int, float]:
    """Finds minimum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return min(array_abs)


def has_negative_number(array: List[Union[int, float]]) -> bool:
    for number in array:
        if number < 0:
            return True
    return False


def has_positive_number(array: List[Union[int, float]]) -> bool:
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


def linspace_by_index(
        array: List[Any],
        how_many: int,
    ) -> List[Any]:
    """
    Gets linspaced values from array (based on indices of the array).
    >>> array = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96]
    >>> linspace_by_index(array=array, how_many=4) # Returns [0, 32, 64, 96]
    >>> linspace_by_index(array=array, how_many=5) # Returns [0, 24, 48, 72, 96]
    """
    linspaced_indices = list(np.linspace(start=0, stop=len(array) - 1, num=how_many))
    linspaced_indices = list(map(np.ceil, linspaced_indices))
    linspaced_indices = list(map(int, linspaced_indices))
    linspaced_values = [array[idx] for idx in linspaced_indices]
    return linspaced_values


def spread_array_by_factor(
        array: List[Union[int, float]],
        factor: int,
    ) -> List[Union[int, float]]:
    """
    Spread out an array by given factor.
    >>> spread_array_by_factor(array=[4, 6, 7, 3], factor=3)
    >>> [4, 4, 4, 6, 6, 6, 7, 7, 7, 3, 3, 3]
    """
    array_after_spreading = []
    for idx, _ in enumerate(array):
        array_after_spreading += [array[idx]] * int(factor)
    return array_after_spreading


def spread_array_by_length(
        array: List[Union[int, float]],
        to: int,
    ) -> List[Union[int, float]]:
    """
    Definition:
        Spread out an array to particular length without distorting signal of the original data.
    Parameters:
        - array (list): List or list-like array data
        - to (int): Length of array to be spread into
    >>> spread_array_by_length(array=[2, 3, -7], to=14)
    >>> [2, 2, 2, 2, 3, 3, 3, 3, 3, -7, -7, -7, -7, -7]
    """
    initial_array_length = len(array)
    if initial_array_length >= to:
        return array
    array_after_spread = []
    spread_factor = to / initial_array_length
    # If length of array to spread into is divisible by length of initial array
    if int(spread_factor) == spread_factor:
        array_after_spread = spread_array_by_factor(array=array, factor=int(spread_factor))
        return array_after_spread
    # Perform necessary complete fill-ups of the array to spread into
    num_complete_fillups = int(np.floor(spread_factor))
    if num_complete_fillups > 0:
        array_after_spread = spread_array_by_factor(array=array, factor=num_complete_fillups)
    # Fill-up the remaining elements of `array_after_spread` randomly (to minimise distortion)
    while len(array_after_spread) != to:
        random_index = random.randint(0, len(array_after_spread)-1)
        random_element = array_after_spread[random_index]
        array_after_spread.insert(random_index+1, random_element)
    return array_after_spread


def normalize_array(array: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Normalizes values in array to range of [0, 1].
    Ignores and removes all NaNs.
    """
    array = np.array(array)
    array = array[~np.isnan(array)]
    normalized_array = (array - np.min(array)) / np.ptp(array)
    return list(normalized_array)


def filter_list_by_offset(
        list_obj: List[Any],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Any]:
    """
    Filters list object based on `offset` and `limit`.
    Note:
        - Default offset is 1
        - Default limit is 25
        - Maximum limit is 25
    """
    default_offset = 1
    default_limit = 25
    max_limit = 25 # Value of `max_limit` must be >= `default_limit`
    if not offset:
        offset = default_offset
    if not limit:
        limit = default_limit
    if offset <= 0:
        offset = default_offset
    if limit <= 0:
        limit = default_limit
    if limit > max_limit:
        limit = max_limit
    list_obj_filtered = list_obj[offset - 1 : offset + limit - 1]
    return list_obj_filtered