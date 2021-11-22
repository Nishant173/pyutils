def __raise_error_if_num_chars_is_negative(num_chars: int) -> None:
    if num_chars < 0:
        raise ValueError(f"Expected `num_chars` to be >= 0, but got {num_chars}")
    return None


def get_first_n_characters(text: str, num_chars: int) -> str:
    __raise_error_if_num_chars_is_negative(num_chars=num_chars)
    return text[:num_chars]


def get_last_n_characters(text: str, num_chars: int) -> str:
    __raise_error_if_num_chars_is_negative(num_chars=num_chars)
    return text[-num_chars:]


def remove_first_n_characters(text: str, num_chars: int) -> str:
    __raise_error_if_num_chars_is_negative(num_chars=num_chars)
    return text[num_chars:]


def remove_last_n_characters(text: str, num_chars: int) -> str:
    __raise_error_if_num_chars_is_negative(num_chars=num_chars)
    return text[:-num_chars]