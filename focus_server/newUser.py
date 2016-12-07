#!/usr/bin/env python

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

''' *** List of accessible api urls ***

*** NOTE: until Akash finishes user authentication/security, <string:id> will
    be the name of the user


1. '/' is a get request that tests accessibility to the flask server
2. '/view/' is a get request that returns all the documents (with _id = 'id')
    in the database
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
   if that app does not yet exist, creates it in the database, and then updates
   the current day to reflect the json usage data sent by the put request


Database Structure - refer to indents as higherarchy

** Inside each document is a dictionary of dictionaries. **

globalopts.appdata Server
    -> database user
        -> user titled documents within database
            -> _id
            -> _rev
            -> appdata
                -> total
                    -> S : value
                    -> M : value
                    -> T : value
                    -> W : value
                    -> R : value
                    -> F : value
                    -> tot : value
                -> Repeat for each app
            -> goals
                -> daily : value
                -> weekly : value

'''


@app.route('/')
def welcome():
    return "Welcome to Focus" + "\n"


# curl -X GET http://localhost:5000/view/
@app.route('/view/', methods=['GET'])
def getDocs():
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
    elif w_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n"
    else:
        return "Daily Time = " + str(data[today_index]) + "\n" + \
               "Weekly Time = " + str(data['tot']) + "\n" + \
               "No goals exceeded! Good job not procrastinating!" + "\n"


# curl -H "Content-type: application/json" -H "Authorization: <auth_token>" \
# -X PUT http://127.0.0.1:5000/usage/Byron/ -d '{"Instagram": 5}'
@app.route('/usage/', methods=['PUT'])
@require_auth_header
def updateUsage():
    now = datetime.datetime.now()
    day = now.strftime("%a")  # gives current day of week abbrev
    # converts to day of week as referenced in the database
    today_index = dayToIndex(day)
    doc = globalopts.appdata.get(request.user)
    # converts the incoming json request to a json dictionary
    jdata = json.loads(request.data)

    for app in jdata:
        if app not in doc:
            # if not in 'appdata', then insert the app by calling the
            # app function before updating usage in database
            app(request.user, app)
            # have to update doc in this case
            doc = globalopts.appdata.get(request.user)
        index = str(app)
        doc['appdata'][index][today_index] = jdata[index]

    globalopts.appdata[request.user] = doc

    # confimation that the json data was received
    return "Hello " + str(jdata) + "\n"

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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
