class InvalidDataFrameError(Exception):
    """Error raised when an Invalid DataFrame is encountered (based on certain expectations)"""
    pass


class MissingRequiredParameterError(Exception):
    """Error raised when a required parameter is missing"""
    pass