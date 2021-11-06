from typing import Callable, Optional
import functools
import traceback

from django.db import (
    connection,
    reset_queries,
)
from rest_framework import status
from rest_framework.response import Response

from pyutils.frameworks.django_ops.utils import get_django_request_info_from_args


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


def api_endpoint_exception_handler(
        api_endpoint_description: str,
        print_response: Optional[bool] = False,
    ) -> Callable:
    """
    Decorator that handles exceptions that may occur in function based API endpoints.
    Expects a function that takes in a `rest_framework.request.Request` object, and
    returns a `rest_framework.response.Response` object.
    If an exception is encountered, then a response with status code 500 is returned.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            try:
                response_obj = func(*args, **kwargs)
                return response_obj
            except Exception as exc:
                response = {
                    'exception_type': type(exc).__name__,
                    'exception_msg': ' | '.join(exc.args),
                    'api_endpoint_function_name': func.__name__,
                    'api_endpoint_description': api_endpoint_description,
                    'traceback_string': traceback.format_exc(),
                    'request_info': get_django_request_info_from_args(*args),
                }
                if print_response:
                    print(f"An exception occurred. Response: {response}")
                return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return wrapper
    return decorator