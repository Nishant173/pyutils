def get_first_n_characters(text: str, num_chars: int) -> str:
    return text[:num_chars]


def get_last_n_characters(text: str, num_chars: int) -> str:
    return text[-num_chars:]


def remove_first_n_characters(text: str, num_chars: int) -> str:
    return text[num_chars:]


def remove_last_n_characters(text: str, num_chars: int) -> str:
    return text[:-num_chars]