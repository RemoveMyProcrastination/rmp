"""

    globalopts.py
    author: Akash Gaonkar

    Global values for the app.

"""

import couchdb


USERS_DOC = 'users'
APPDATA_DOC = 'appdata'

db = couchdb.Server()
users = db[USERS_DOC] if USERS_DOC in db else db.create(USERS_DOC)
appdata = db[APPDATA_DOC] if APPDATA_DOC in db else db.create(APPDATA_DOC)

# Defines a valid username
REGEX_USERNAME = r'([a-zA-Z0-9 _\-@.]){6,}'

# Weekly Time holders for each app
DEFAULT_WEEKLY_TIMES = \
    {'S': 0, 'M': 0, 'T': 0, 'W': 0, 'R': 0, 'F': 0, 'Sa': 0, 'tot': 0}

DEFAULT_GOALS = {'daily': 24, 'weekly': 150}
# goals are unreachable so notifications have to be set first
