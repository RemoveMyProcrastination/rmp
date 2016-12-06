#!/usr/bin/env python

from flask import Flask, request
import couchdb, json, datetime
app = Flask(__name__)

''' *** List of accessible api urls ***

***NOTE: until Akash finishes user authentication/security, <string:id> will be the name of the user


1. '/' is a get request that tests accessibility to the flask server
2. '/view/' is a get request that returns all the documents (with _id = 'id') in the database
3. '/get/<string:userid>/' is a get request that returns all of the information in the database corresponding to a specific userid user including goals, _id, _rev, etc.
4. '/getapps/<string:userid>/' is a get request that returns only the application data dictionary
5. '/newuser/<string:userid>/' is a put request that creates a new user
6. '/app/<string:userid>/<string:app>' is open to both PUT and DELETE requests
    a. the PUT request places that app in the database if not already present, otherwise does nothing to prevent overriding data that may exist
    b. the DELETE request removes the app from the database if present
7. '/getgoal/<string:userid>/' is a get request that retrieves the Daily and Weekly Goals from the server
8. '/newgoal/<string:userid>/<int:daily>/<int:weekly>/' is a put requests that can be used to set new goals
9. '/usage/<string:userid>/' is a put request that takes in json usage data and if that app does not yet exist, creates it in the database, and then updates the current day to reflect the json usage data sent by the put request


Database Structure - refer to indents as higherarchy

** Inside each document is a dictionary of dictionaries. **
    
Couchdb Server
    -> database userid
        -> user titled documents within database
            -> _id
            -> _rev
            -> Appdata
                -> Total
                    -> S : value
                    -> M : value
                    -> T : value
                    -> W : value
                    -> R : value
                    -> F : value
                    -> Tot : value
                -> Repeat for each app
            -> Goals
                -> Daily : value
                -> Weekly : value

'''

server = couchdb.Server()
db = server['test']
headers = {'Content-Type': 'application/json'}
Weekly = {'S': 0, 'M': 0, 'T': 0, 'W': 0, 'R': 0, 'F': 0, 'Sa': 0, 'Tot': 0} 
#Weekly Time holders for each app
Goals = {'Daily': 24, 'Weekly': 150}    
#make goals unreachable so notifications have to be set first

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

def appTotal(Appdata):    

    for app, data in Appdata.items():
        print(data)
        total = 0
        if app != 'Total':
            for day, hours in data.items():
                print(hours)
                if day != 'Tot':        #updates the total usage in each respective App dictionary
                    total += int(hours)
            data['Tot'] = total         #updates total for that app

    weekly = 0
    for day in Weekly:
        today = 0 
        if day != 'Tot':
            for app, data in Appdata.items():
                if day != 'Tot':
                    today += data[day]
            Appdata['Total'][day] = today      #updates total for the day  
            weekly += today             
    Appdata['Total']['Tot'] = weekly        #updates weekly total
    return Appdata 

@app.route('/')
def welcome():
    return "Welcome to Focus" + "\n"

@app.route('/view/', methods = ['GET'])
#curl -X GET http://localhost:5000/view/    

def getDocs():
    return json.dumps(db.get('_all_docs')) + "\n"

@app.route('/get/<string:userid>/', methods = ['GET'])
#curl -X GET http://localhost:5000/get/<userid>/ 

def getName(userid):
    if userid in db:
        doc = db.get(userid)
        doc['Appdata'] = appTotal(doc['Appdata']) 
        db[userid] = doc
        return json.dumps(db.get(userid)) + "\n"
    else:
        return "User not in database"

@app.route('/getapps/<string:userid>/', methods = ['GET'])
#curl -X GET http://localhost:5000/get/<userid>/    

def getApps(userid):
    if userid in db:
        doc = db.get(userid)
        doc['Appdata'] = appTotal(doc['Appdata']) 
        db[userid] = doc
        return json.dumps(db.get(userid)['Appdata']) + "\n"
    else:
        return "User not in database"

@app.route('/newuser/<string:userid>/', methods = ['PUT'])
#curl -X PUT http://localhost:5000/newuser/<userid>/    

def newUser(userid):
    if userid in db:
        return userid + " already in db!" + "\n"
    db[userid] = {'userid': userid, 'Appdata': {'Total': Weekly}, 'Goals': Goals}
    if userid in db:
        return "Successfully inserted " + userid + "\n"
    else:
        return "Failed to insert"
    

@app.route('/app/<string:userid>/<string:app>/', methods = ['PUT','DELETE'])

def App(userid,app): 
    doc = db.get(userid)
    if request.method == "PUT":
        #curl -X PUT http://localhost:5000/app/<userid>/<app>/    
        if app in doc['Appdata']:
            return app + " already in Appdata" + "\n"
        else:
            doc['Appdata'][app] = Weekly
            db[userid] = doc
            return "Successfully inserted " + app + "\n" 
    elif request.method == "DELETE":
        #curl -X DELETE http://localhost:5000/app/<userid>/<app>/ 
        if app in doc['Appdata']:
            del doc['Appdata'][app]
            db[userid] = doc
            return "Successfully deleted " + app + "\n"
        else:
            return app + " not in Appdata" + "\n"

@app.route('/getgoal/<string:userid>/', methods = ['GET'])
#curl -X GET http://localhost:5000/getgoal/<userid>/ 

def getGoal(userid):
    doc = db.get(userid)
    return "Daily Goal is : " + str(doc['Goals']['Daily']) + "\n" + "Weekly Goal is : " + str(doc['Goals']['Weekly']) + "\n"

@app.route('/newgoal/<string:userid>/<int:daily>/<int:weekly>/', methods = ['PUT'])
#curl -X PUT http://localhost:5000/newgoal/<userid>/<daily>/<weekly>/ 

def newGoal(userid,daily,weekly):
    doc = db.get(userid)
    doc['Goals']['Daily'] = daily 
    doc['Goals']['Weekly'] = weekly
    db[userid] = doc
    return "New Daily is: " + str(daily) + "\n" + "New Weekly is: " + str(weekly) + "\n"
    
@app.route('/dgraph/<string:userid>/', methods = ['GET'])

#The following 2 functions, which were just implemented return the daily and weekly lists that will be used for their corresponding graph inputs 

def dailyGraph(userid):

    now = datetime.datetime.now()
    day = now.strftime("%a")
    today = dayToIndex(day)
    doc = db.get(userid)
    dailylist = []
    for app in doc['Appdata']:
        if app != "Total":
            #print(app)
            
            dailylist.append((doc['Appdata'][app][today], app))
    dailylist = sorted(dailylist)
    dailylist.append((doc['Appdata']['Total'][today], "Total"))
    dailylist.append((doc['Goals']['Daily'], "Goal"))
    #print (dailylist)

    return str(dailylist) + "\n"


def weeklyGraph(userid):

    weeklylist = []
    for day in Weekly:
        if day != "Tot":
            weeklylist.append((doc['Appdata']['Total'][day]))
    weeklylist = sorted(weeklylist)
    weeklylist.append((doc['Appdata']['Total']['Tot'], "Total"))
    weeklylist.append((doc['Goals']['Weekly'], "Goal"))

    return str(weeklylist) + "\n"
    
    


app.route('/compare/<string:userid>/', methods = ['GET'])    
#curl -X GET http://localhost:5000/compare/<userid>

def checker(userid):
    #https://www.tutorialspoint.com/python/time_strftime.htm
    now = datetime.datetime.now()
    day = now.strftime("%a")      #gives current day of week abbrev
    doc = db.get(userid)
    data = doc['Appdata']['Total']
    w_excess = data['Tot'] - doc['Goals']['Weekly']
    today_index = dayToIndex(day)
    d_excess = data[today_index] - doc['Goals']['Daily']
    
    if w_excess > 0 and d_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n" + \
        "Daily limit exceeded by " + str(d_excess) + "\n"
    elif d_excess > 0:
        return "Daily limit exceeded by " + str(d_excess) + "\n"
    elif w_excess > 0: 
        return "Weekly limit exceeded by " + str(w_excess) + "\n"
    else:
        return "Daily Time = " + str(data[today_index]) + "\n" + \
        "Weekly Time = " + str(data['Tot']) + "\n" + \
        "No goals exceeded! Good job not procrastinating!" + "\n"

@app.route('/usage/<string:userid>/', methods = ['PUT'])      
# curl -H "Content-type: application/json" -X PUT http://127.0.0.1:5000/usage/Byron/ -d '{"Instagram": 5}'

def takeJson(userid):
    now = datetime.datetime.now()
    day = now.strftime("%a")            #gives current day of week abbrev
    today_index = dayToIndex(day)       #converts to day of week as referenced in the database
    doc = db.get(userid)  
    jdata = json.loads(request.data)    #converts the incoming json request to a json dictionary

    for app in jdata:       
        if app not in doc:              #if not in 'Appdata', then insert the app by calling the App function before updating usage in database 
            App(userid,app)
            doc = db.get(userid)        #have to update doc in this case 
        index =  str(app)
        doc['Appdata'][index][today_index] = jdata[index] 


    db[userid] = doc

    return "Hello " + str(jdata) + "\n"     #confimation that the json data was received
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
