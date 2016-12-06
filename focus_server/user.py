"""
    user.py
    author: Akash Gaonkar

    Manages user login and creation.
"""

from flask import Blueprint, request

import auth
import globalopts
from util import create_error, require_json_with_args


blueprint_user = Blueprint('user', __name__)


@blueprint_user.route('/login/', methods=['POST'])
@require_json_with_args('username', 'password')
def login():
    """ Logs in a user.

        On success returns an authorization token, which must then be sent
        up with every call requiring authorization.

        On failure returns a 401 NOT AUTHORIZED.

        Ex: (assumes prefix is localhost:5000/user/)
        ```
        curl -X POST -H "Content-Type: application/json" \
        localhost:5000/user/login/ -d '{
            "username": "johndoe",
            "password": "hello world"
        }'; echo ''
        ```
    """

    username = str(request.parsed_json['username'])
    password = str(request.parsed_json['password'])

    if not auth.check_password(username, password):
        return create_error(401, "login failed")

    return auth.create_auth_token(username, password), 200


@blueprint_user.route('/', methods=['POST'])
@require_json_with_args('email', 'username', 'password')
def create_user():
    """ Creates a user.

        On failure returns 400 and error.
        On success, returns 200.

        Ex: (assumes prefix is localhost:5000/user/)
        ```
        curl -X POST -H "Content-Type: application/json" \
        localhost:5000/user/ -d '{
            "username": "johndoe",
            "password": "hello world",
            "email": "jdoe@gmail.com"
        }'; echo ''
        ```
    """

    username = str(request.parsed_json['username'])
    email = str(request.parsed_json['email'])
    password = str(request.parsed_json['password'])

    res = auth.create_user(username, email, password)
    if not res:
        return create_error(400, str(res))

    globalopts.appdata[username] = {
        'user': username,
        'Appdata': {'Total': globalopts.DEFAULT_WEEKLY_TIMES},
        'Goals': [globalopts.DEFAULT_GOALS]
    }

    print(globalopts.appdata[username])

    return "", 200


@blueprint_user.route('/', methods=['DELETE'])
@auth.require_auth_header
def delete_user():
    """ Deletes a user.

        On success, returns 200
    """
    del globalopts.appdata[request.user]
    del globalopts.users[request.user]
    return "", 200
