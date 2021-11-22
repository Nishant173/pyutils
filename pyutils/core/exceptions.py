from typing import Any, List


def raise_exception_if_invalid_option(
        option_name: str,
        option_value: Any,
        valid_option_values: List[Any],
    ) -> None:
    """Raises a ValueError if the `option_value` given is an invalid option; otherwise returns None"""
    if option_value not in valid_option_values:
        raise ValueError(f"Expected `{option_name}` to be in {valid_option_values}, but got {option_value}")
    return None


class InvalidDataFrameError(Exception):
    """Error raised when an Invalid DataFrame is encountered (based on certain expectations)"""
    pass


class MissingRequiredParameterError(Exception):
    """Error raised when a required parameter is missing"""
    pass