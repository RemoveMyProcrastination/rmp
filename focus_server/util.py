"""

    util.py
    author: Akash Gaonkar

    Generic helper methods.

"""

from functools import wraps
from flask import request
import json
import sys


def require_json_with_args(*required):
    """ Ensures that a request is json and has the required arguments.

        Sets request.parsed_json to the parsed version of the json.

        Usage:
        ```
        @app.route('/some_route/')
        @require_json_with_args('blah')
        def route_handler():
            # ...
            pass
        ```
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request.parsed_json = request.get_json()
                for r in required:
                    if not request.parsed_json or r not in request.parsed_json:
                        return create_error(
                            400, 'missing json argument: \'%s\'' % r
                        )
                return func(*args, **kwargs)
            except ValueError as err:
                return create_error(400, 'invalid json: %s' % err)
        return wrapper
    return decorator


def create_error(code=400, msg='bad request'):
    """ Creates a json error with a given HTTP error code.

        Can be directly returned from a flask request handler.

        Args:
            code: The error code to be returned.
            msg: The message to be used.

        Returns:
            A tuple of a JSON string and the error code.

    """
    return json.dumps({'status': code, 'error': msg}), code


def print_and_flush(*args):
    """ Prints and flushes the stdout buffer to help with debugging. """
    print(*args)
    sys.stdout.flush()
