#!/usr/bin/env python

<<<<<<< HEAD
from flask import Flask, request
import couchdb
import json
import datetime

app = Flask(__name__)
=======
"""

    newUser.py
    author: Byron Becker
    author: Akash Gaonkar -- added user authentication

    Creates and runs the flask server.

"""

import json
import datetime
from flask import Flask, request

import globalopts
from auth import require_auth_header
from user import blueprint_user

app = Flask(__name__)
app.register_blueprint(blueprint_user, url_prefix="/user")
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a

''' *** List of accessible api urls ***

*** NOTE: until Akash finishes user authentication/security, <string:id> will
    be the name of the user


1. '/' is a get request that tests accessibility to the flask server
2. '/view/' is a get request that returns all the documents (with _id = 'id')
    in the database
<<<<<<< HEAD
3. '/get/<string:userid>/' is a get request that returns all of the information
    in the database corresponding to a specific userid user including goals,
    _id, _rev, etc.
4. '/getapps/<string:userid>/' is a get request that returns only the
    application data dictionary
5. '/newuser/<string:userid>/' is a put request that creates a new user
6. '/app/<string:userid>/<string:app>' is open to both PUT and DELETE requests
    a. the PUT request places that app in the database if not already present,
       otherwise does nothing to prevent overriding data that may exist
    b. the DELETE request removes the app from the database if present
7. '/getgoal/<string:userid>/' is a get request that retrieves the Daily and
    Weekly Goals from the server
8. '/newgoal/<string:userid>/<int:daily>/<int:weekly>/' is a put requests that
    can be used to set new goals
9. '/usage/<string:userid>/' is a put request that takes in json usage data and
=======
3. '/get/' is a get request that returns all of the information
    in the database corresponding to a specific user user including goals,
    _id, _rev, etc.
4. '/apps/' is a get request that returns only the
    application data dictionary
5. '/user/' is a put request that creates a new user
6. '/app/<string:app>' is open to both PUT and DELETE requests
    a. the PUT request places that app in the database if not already present,
       otherwise does nothing to prevent overriding data that may exist
    b. the DELETE request removes the app from the database if present
7. '/getgoal/' is a get request that retrieves the daily and
    weekly goals from the server
8. '/newgoal/<int:daily>/<int:weekly>/' is a put requests that
    can be used to set new goals
9. '/usage/' is a put request that takes in json usage data and
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
   if that app does not yet exist, creates it in the database, and then updates
   the current day to reflect the json usage data sent by the put request


Database Structure - refer to indents as higherarchy

** Inside each document is a dictionary of dictionaries. **

<<<<<<< HEAD
Couchdb Server
    -> database userid
        -> user titled documents within database
            -> _id
            -> _rev
            -> Appdata
                -> Total
=======
globalopts.appdata Server
    -> database user
        -> user titled documents within database
            -> _id
            -> _rev
            -> appdata
                -> total
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
                    -> S : value
                    -> M : value
                    -> T : value
                    -> W : value
                    -> R : value
                    -> F : value
<<<<<<< HEAD
                    -> Tot : value
                -> Repeat for each app
            -> Goals
                -> Daily : value
                -> Weekly : value
=======
                    -> tot : value
                -> Repeat for each app
            -> goals
                -> daily : value
                -> weekly : value
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a

'''


<<<<<<< HEAD
server = couchdb.Server()
dbname = 'test'

db = server[dbname] if dbname in server else server.create(dbname)


headers = {'Content-Type': 'application/json'}
weekly = {'S': 0, 'M': 0, 'T': 0, 'W': 0, 'R': 0, 'F': 0, 'Sa': 0, 'Tot': 0}
# Weekly Time holders for each app
goals = {'daily': 24, 'weekly': 150}
# make goals unreachable so notifications have to be set first


def dayToIndex(day):
    switcher = {
        'Mon': 'M',
        'Tue': 'T',
        'Wed': 'W',
        'Thu': 'R',
        'Fri': 'F',
        'Sat': 'Sa',
        'Sun': 'S'
    }

    return switcher.get(day, "nothing")


=======
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
@app.route('/')
def welcome():
    return "Welcome to Focus" + "\n"


# curl -X GET http://localhost:5000/view/
@app.route('/view/', methods=['GET'])
def getDocs():
<<<<<<< HEAD
    return json.dumps(db.get('_all_docs')) + "\n"


# curl -X GET http://localhost:5000/get/<userid>/
@app.route('/get/<string:userid>/', methods=['GET'])
def getName(userid):
    if userid in db:
        return json.dumps(db.get(userid)) + "\n"
    else:
        return "User not in database"


# curl -X GET http://localhost:5000/get/<userid>/
@app.route('/getapps/<string:userid>/', methods=['GET'])
def getApps(userid):
    if userid in db:
        return json.dumps(db.get(userid)['Appdata']) + "\n"
    else:
        return "User not in database"


# curl -X PUT http://localhost:5000/newuser/<userid>/
@app.route('/newuser/<string:userid>/', methods=['PUT'])
def newUser(userid):
    if userid in db:
        return userid + " already in db!" + "\n"
    db[userid] = {
        'userid': userid,
        'Appdata': {'Total': weekly},
        'Goals': goals
    }
    if userid in db:
        return "Successfully inserted " + userid + "\n"
    else:
        return "Failed to insert"


@app.route('/app/<string:userid>/<string:app>/', methods=['PUT', 'DELETE'])
def App(userid, app):
    doc = db.get(userid)
    if request.method == "PUT":
        # curl -X PUT http://localhost:5000/app/<userid>/<app>/
        if app in doc['Appdata']:
            return app + " already in Appdata" + "\n"
        else:
            doc['Appdata'][app] = weekly
            db[userid] = doc
            return "Successfully inserted " + app + "\n"
    elif request.method == "DELETE":
        # curl -X DELETE http://localhost:5000/app/<userid>/<app>/
        if app in doc['Appdata']:
            del doc['Appdata'][app]
            db[userid] = doc
            return "Successfully deleted " + app + "\n"
        else:
            return app + " not in Appdata" + "\n"


# curl -X GET http://localhost:5000/getgoal/<userid>/
@app.route('/getgoal/<string:userid>/', methods=['GET'])
def getGoal(userid):
    doc = db.get(userid)
    return "Daily Goal is : " + str(doc['Goals']['Daily']) + "\n" + \
           "Weekly Goal is : " + str(doc['Goals']['Weekly']) + "\n"


# curl -X PUT http://localhost:5000/newgoal/<userid>/<daily>/<weekly>/
@app.route(
    '/newgoal/<string:userid>/<int:daily>/<int:weekly>/', methods=['PUT']
)
def newGoal(userid, daily, weekly):
    doc = db.get(userid)
    doc['Goals']['Daily'] = daily
    doc['Goals']['Weekly'] = weekly
    db[userid] = doc
    return "New Daily is: " + str(daily) + "\n" + \
           "New Weekly is: " + str(weekly) + "\n"


# curl -X GET http://localhost:5000/compare/<userid>
@app.route('/compare/<string:userid>/', methods=['GET'])
def checker(userid):
    # https://www.tutorialspoint.com/python/time_strftime.htm
    now = datetime.datetime.now()
    day = now.strftime("%a")      # gives current day of week abbrev
    doc = db.get(userid)
    data = doc['Appdata']['Total']
    w_excess = data['Tot'] - doc['Goals']['Weekly']
    today_index = dayToIndex(day)
    d_excess = data[today_index] - doc['Goals']['Daily']

    if w_excess > 0 and d_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n" + \
               "Daily limit exceeded by " + (d_excess) + "\n"
    elif d_excess > 0:
        return "Daily limit exceeded by " + (d_excess) + "\n"
=======
    return json.dumps(globalopts.appdata.get('_all_docs')) + "\n"


# curl -X GET http://localhost:5000/get/
@app.route('/get/', methods=['GET'])
@require_auth_header
def getName():
    doc = globalopts.appdata[request.user]
    doc['Appdata'] = appTotal(doc['Appdata'])
    globalopts.appdata[request.user] = doc
    return json.dumps(globalopts.appdata[request.user])


# curl -X GET -H "Authorization: <auth_token>" http://localhost:5000/apps/
@app.route('/apps/', methods=['GET'])
@require_auth_header
def getApps():
    doc = globalopts.appdata[request.user]
    doc['Appdata'] = appTotal(doc['Appdata'])
    globalopts.appdata[request.user] = doc
    return json.dumps(globalopts.appdata[request.user]['Appdata'])


# curl -X PUT -H "Authorization: <auth_token>" http://localhost:5000/app/<app>/
@app.route('/app/<string:app>/', methods=['PUT'])
@require_auth_header
def add_app(app):
    doc = globalopts.appdata.get(request.user)
    if app in doc['appdata']:
        return app + " already in appdata" + "\n"
    else:
        doc['appdata'][app] = globalopts.DEFAULT_WEEKLY_TIMES
        globalopts.appdata[request.user] = doc
        return "Successfully inserted " + app + "\n"


# curl -X DELETE -H "Authorization: <auth_token>" \
# http://localhost:5000/app/<app>/
@app.route('/app/<string:app>/', methods=['DELETE'])
@require_auth_header
def delete_app(app):
    doc = globalopts.appdata.get(request.user)
    if app in doc['appdata']:
        del doc['appdata'][app]
        globalopts.appdata[request.user] = doc
        return "Successfully deleted " + app + "\n"
    else:
        return app + " not in appdata" + "\n"


# curl -X GET -H "Authorization: <auth_token>" http://localhost:5000/getgoal/
@app.route('/getgoal/', methods=['GET'])
@require_auth_header
def getGoal():
    doc = globalopts.appdata.get(request.user)
    return "Daily Goal is : " + str(doc['goals']['daily']) + "\n" + \
           "Weekly Goal is : " + str(doc['goals']['weekly']) + "\n"


# curl -X -H "Authorization: <auth_token>" \
# PUT http://localhost:5000/newgoal/<daily>/<weekly>/
@app.route('/newgoal/<int:daily>/<int:weekly>/', methods=['PUT'])
@require_auth_header
def newGoal(daily, weekly):
    doc = globalopts.appdata.get(request.user)
    doc['goals']['daily'] = daily
    doc['goals']['weekly'] = weekly
    globalopts.appdata[request.user] = doc
    return "New daily is: " + str(daily) + "\n" + \
           "New weekly is: " + str(weekly) + "\n"

@app.route('/dgraph/', methods=['GET'])
@require_auth_header
def dailyGraph():
#curl -X GET http://localhost:5000/dgraph/<userid>/

    now = datetime.datetime.now()
    day = now.strftime("%a")
    today = dayToIndex(day)
    doc = db.get(request.user)
    apps = []
    dailylist = {}
    for app in doc['Appdata']:
        if app != "Total":
            apps.append((doc['Appdata'][app][today], app))
    apps = sorted(apps)
    dailylist["apps"] = apps
    dailylist["total"] = ((doc['Appdata']['Total'][today], "Total"))
    dailylist["goals"] = ((doc['Goals']['Daily'], "Goal"))
    return json.dumps(dailylist)

@app.route('/wgraph/', methods=['GET'])
@require_auth_header
def weeklyGraph():
#curl -X GET http://localhost:5000/wgraph/<userid>/

    doc = db.get(request.user)
    weeklylist = {}
    days = []
    for day in weeksort:
        if day != 'Tot':
            days.append((doc['Appdata']['Total'][day], day))

    weeklylist["days"] = days 
    weeklylist["total"] = ((doc['Appdata']['Total']['Tot'], "Total"))
    weeklylist["goals"] = ((doc['Goals']['Weekly'], "Goal"))

    return json.dumps(weeklylist)

# curl -X -H "Authorization: <auth_token>" GET http://localhost:5000/compare
@app.route('/compare/', methods=['GET'])
@require_auth_header
def checker():
    # https://www.tutorialspoint.com/python/time_strftime.htm
    now = datetime.datetime.now()
    day = now.strftime("%a")      # gives current day of week abbrev
    doc = globalopts.appdata.get(request.user)
    data = doc['appdata']['total']
    w_excess = data['tot'] - doc['goals']['weekly']
    today_index = dayToIndex(day)
    d_excess = data[today_index] - doc['goals']['daily']

    if w_excess > 0 and d_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n" + \
               "Daily limit exceeded by " + str(d_excess) + "\n"
    elif d_excess > 0:
        return "Daily limit exceeded by " + str(d_excess) + "\n"
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
    elif w_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n"
    else:
        return "Daily Time = " + str(data[today_index]) + "\n" + \
<<<<<<< HEAD
               "Weekly Time = " + str(data['Tot']) + "\n" + \
               "No goals exceeded! Good job not procrastinating!" + "\n"


# curl -H "Content-type: application/json" -X PUT
#   http://127.0.0.1:5000/usage/Byron/ -d '{"Instagram": 5}'
@app.route('/usage/<string:userid>/', methods=['PUT'])
def takeJson(userid):
=======
               "Weekly Time = " + str(data['tot']) + "\n" + \
               "No goals exceeded! Good job not procrastinating!" + "\n"


# curl -H "Content-type: application/json" -H "Authorization: <auth_token>" \
# -X PUT http://127.0.0.1:5000/usage/Byron/ -d '{"Instagram": 5}'
@app.route('/usage/', methods=['PUT'])
@require_auth_header
def updateUsage():
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
    now = datetime.datetime.now()
    day = now.strftime("%a")  # gives current day of week abbrev
    # converts to day of week as referenced in the database
    today_index = dayToIndex(day)
<<<<<<< HEAD
    doc = db.get(userid)
=======
    doc = globalopts.appdata.get(request.user)
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a
    # converts the incoming json request to a json dictionary
    jdata = json.loads(request.data)

    for app in jdata:
        if app not in doc:
<<<<<<< HEAD
            # if not in 'Appdata', then insert the app by calling the
            # App function before updating usage in database
            App(userid, app)
            doc = db.get(userid)  # have to update doc in this case
        index = str(app)
        doc['Appdata'][index][today_index] = jdata[index]

    db[userid] = doc
=======
            # if not in 'appdata', then insert the app by calling the
            # app function before updating usage in database
            app(request.user, app)
            # have to update doc in this case
            doc = globalopts.appdata.get(request.user)
        index = str(app)
        doc['appdata'][index][today_index] = jdata[index]

    globalopts.appdata[request.user] = doc
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a

    # confimation that the json data was received
    return "Hello " + str(jdata) + "\n"

<<<<<<< HEAD
=======
@app.route('/clear/', methods = ['PUT'])
@require_auth_header
def clearData():
    doc = db.get(request.user)
    for app, data in doc['Appdata'].items():        #algorithm runs in 8 * (number of apps + 1) time
        for day in data:
            data[day] = 0
    db[userid] = doc 
    return json.dumps(doc)


def dayToIndex(day):
    switcher = {
        'Mon': 'M',
        'Tue': 'T',
        'Wed': 'W',
        'Thu': 'R',
        'Fri': 'F',
        'Sat': 'Sa',
        'Sun': 'S'
    }

    return switcher.get(day, "nothing")


def appTotal(appdata):
    for app, data in appdata.items():
        total = 0
        if app != 'Total':
            for day, hours in data.items():
                if day != 'Tot':
                    # updates the total usage in each respective App dictionary
                    total += hours
            data['Tot'] = total  # updates total for that app

    weekly = 0
    for day in globalopts.DEFAULT_WEEKLY_TIMES:
        today = 0
        if day != 'Tot':
            for app, data in appdata.items():
                if app != 'Total':
                    today += data[day]
            appdata['Total'][day] = today  # updates total for the day
            weekly += today
    appdata['Total']['Tot'] = weekly  # updates weekly total
    return appdata

>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
