from typing import Callable
import functools

from django.db import (
    connection,
    reset_queries,
)


def django_query_counter(func: Callable) -> Callable:
    """Decorator that prints the number of Django queries executed by the decorated function"""
    @functools.wraps(func)
    def wrapper_django_query_counter(*args, **kwargs):
        reset_queries()
        num_queries_at_start = len(connection.queries)
        result = func(*args, **kwargs)
        num_queries_at_end = len(connection.queries)
        num_queries = num_queries_at_end - num_queries_at_start
        print(
            f"Number of Django queries executed by function {func.__name__!r} is: {num_queries}"
        )
        return result
    return wrapper_django_query_counter