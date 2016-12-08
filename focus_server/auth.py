"""
    auth.py
    author: Akash Gaonkar

    Methods to help with user authentication.

    Some useful methods:
    create_user: add a new user to the users document
    check_password: check a username and password
    create_auth_token: create an authorization token
    @require_auth_header: ensure an auth token is sent with a
        request. this will also set request.user to be the
        logged in user if Successful.
"""

import bcrypt
import re
from base64 import b64encode, b64decode
from flask import request
from functools import wraps

import globalopts
from util import create_error

AUTH_HEADER = 'Authorization'

REGEX_EMAIL = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


class AuthError(Exception):
    def __bool__(self):
        return False


def require_auth_header(func):
    """ A decorator that ensures a route has a valid authorization header.
        If authorized, the function will sets request.user to hold the
        username of the logged in user.

        Args:
            func: The function to decorate

        Returns:
            A function that validates authorization and then performs func.

        Ex:
        ```
        @app.route('/someroute/')
        @require_auth_header
        def createUser():
            # ...
            pass
        ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if AUTH_HEADER not in request.headers:
            return create_error(401, "no authorization header")

        if not check_auth_token(request.headers[AUTH_HEADER]):
            return create_error(401, "invalid authorization")

        auth_type, key = get_auth_details(request.headers[AUTH_HEADER])
        user, passw = get_credentials(key)
        request.user = user

        return func(*args, **kwargs)

    return wrapper


def create_user(username, email, password):
    """ Creates a user with a given name, email, and password.

        Args:
            username: the string username
            email: the string email of the user
            password: the string password for the user

        Returns:
            True if the user was created, an error (which will evaluate
            to false) otherwise.

    """
    if not re.fullmatch(globalopts.REGEX_USERNAME, username):
        return AuthError("invalid username")

    if username in globalopts.users:
        return AuthError("duplicate username")

    if not re.fullmatch(REGEX_EMAIL, email):
        return AuthError("invalid email")

    if len(password) < 8:
        return AuthError("invalid password")

    password = bytes(password, 'utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    globalopts.users[username] = {
        'name': username,
        'email': email,
        'password': hashed.decode('utf-8')
    }

    return True


def create_auth_token(username, password):
    """ Creates an authorization token from a username and a password.

        Args:
            username: a string username
            password: a string password

        Returns:
            A string auth token.

    """
    return "Basic %s" % (b64encode(
        (username + ':' + password).encode('utf-8')
    ).decode('utf-8'))


def check_auth_token(header, user=None):
    """ Returns whether an auth token is valid for an existing user.

        Args:
            token: a token to validate

        Returns:
            True if the token is valid, False otherwise.

    """
    try:
        auth_type, key = get_auth_details(header)

        if not auth_type == 'Basic':
            return False

        user, passw = get_credentials(key)

        return check_password(str(user), str(passw))

    except:
        return False


def get_auth_details(auth_header):
    """ Returns the authorization type and key from an auth header.

        Args:
            auth_header: the string authorization header

        Returns:
            A tuple of the string auth type and string auth key.

    """
    return auth_header.split(' ', maxsplit=1)


def get_credentials(auth_key):
    """ Returns the username and password from an auth key.

        NOTE: Could throw an error if the token is poorly formatted.

        Args:
            auth_key: the string authorization key

        Returns:
            A tuple of the username and password

    """
    return b64decode(auth_key).decode().split(':')


def check_password(username, password):
    """ Checks to make sure a user with a given username has a given password.

        Args:
            username: a string username
            password: a string password

        Returns:
            True if the password matches the username, False otherwise.
    """
    user = globalopts.users.get(username, None)
    if not user:
        return False

    passw = bytes(password, 'utf-8')
    hashed = user['password'].encode('utf-8')

    return user and hashed == bcrypt.hashpw(passw, hashed)
