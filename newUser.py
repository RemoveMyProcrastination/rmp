#!/usr/bin/env python

from flask import Flask, request
import couchdb, json, datetime
app = Flask(__name__)

''' *** List of accessible api urls ***
1. '/' is a get request that tests accessibility to the flask server
2. '/view/' is a get request that returns all the documents (with _id = 'username') in the database
3. '/get/<string:name>/' is a get request that returns all of the information in the database corresponding to a specific name user including goals, _id, _rev, etc.
4. '/getapps/<string:name>/' is a get request that returns only the application data dictionary
5. '/newuser/<string:name>/' is a put request that creates a new user
6. '/app/<string:name>/<string:app>' is open to both PUT and DELETE requests
    a. the PUT request places that app in the database if not already present, otherwise does nothing to prevent overriding data that may exist
    b. the DELETE request removes the app from the database if present
7. '/getgoal/<string:name>/' is a get request that retrieves the Daily and Weekly Goals from the server
8. '/newgoal/<string:name>/<int:daily>/<int:weekly>/' is a put requests that can be used to set new goals
9. '/usage/<string:name>/' is a put request that takes in json usage data and if that app does not yet exist, creates it in the database, and then updates the current day to reflect the json usage data sent by the put request


Database Structure - refer to indents as higherarchy

** Inside each document is a dictionary of dictionaries. **
    
Couchdb Server
    -> database name
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

@app.route('/')
def welcome():
    return "Welcome to Focus" + "\n"

@app.route('/view/', methods = ['GET'])
#curl -X GET http://localhost:5000/view/    

def getDocs():
    return json.dumps(db.get('_all_docs')) + "\n"

@app.route('/get/<string:name>/', methods = ['GET'])
#curl -X GET http://localhost:5000/get/<name>    

def getName(name):
    if name in db:
        return json.dumps(db.get(name)) + "\n"
    else:
        return "User not in database"

@app.route('/getapps/<string:name>/', methods = ['GET'])
#curl -X GET http://localhost:5000/get/<name>    

def getApps(name):
    if name in db:
        return json.dumps(db.get(name)['Appdata']) + "\n"
    else:
        return "User not in database"

@app.route('/newuser/<string:name>/', methods = ['PUT'])
#curl -X PUT http://localhost:5000/newuser/<name>    

def newUser(name):
    if name in db:
        return name + " already in db!" + "\n"
    db[name] = {'name': name, 'Appdata': {'Total': Weekly}, 'Goals': Goals}
    if name in db:
        return "Successfully inserted " + name + "\n"
    else:
        return "Failed to insert"
    

@app.route('/app/<string:name>/<string:app>/', methods = ['PUT','DELETE'])

def App(name,app): 
    doc = db.get(name)
    if request.method == "PUT":
        #curl -X PUT http://localhost:5000/app/<name>/<app>/    
        if app in doc['Appdata']:
            return app + " already in Appdata" + "\n"
        else:
            doc['Appdata'][app] = Weekly
            db[name] = doc
            return "Successfully inserted " + app + "\n" 
    elif request.method == "DELETE":
        #curl -X DELETE http://localhost:5000/app/<name>/<app>/ 
        if app in doc['Appdata']:
            del doc['Appdata'][app]
            db[name] = doc
            return "Successfully deleted " + app + "\n"
        else:
            return app + " not in Appdata" + "\n"

@app.route('/getgoal/<string:name>/', methods = ['GET'])
#curl -X GET http://localhost:5000/getgoal/<name>/ 

def getGoal(name):
    doc = db.get(name)
    return "Daily Goal is : " + str(doc['Goals']['Daily']) + "\n" + "Weekly Goal is : " + str(doc['Goals']['Weekly']) + "\n"

@app.route('/newgoal/<string:name>/<int:daily>/<int:weekly>/', methods = ['PUT'])
#curl -X PUT http://localhost:5000/newgoal/<name>/<daily>/<weekly>/ 

def newGoal(name,daily,weekly):
    doc = db.get(name)
    doc['Goals']['Daily'] = daily 
    doc['Goals']['Weekly'] = weekly
    db[name] = doc
    return "New Daily is: " + str(daily) + "\n" + "New Weekly is: " + str(weekly) + "\n"
    
@app.route('/compare/<string:name>/', methods = ['GET'])    
#curl -X GET http://localhost:5000/compare/<name>

def checker(name):
    #https://www.tutorialspoint.com/python/time_strftime.htm
    now = datetime.datetime.now()
    day = now.strftime("%a")      #gives current day of week abbrev
    doc = db.get(name)
    data = doc['Appdata']['Total']
    w_excess = data['Tot'] - doc['Goals']['Weekly']
    today_index = dayToIndex(day)
    d_excess = data[today_index] - doc['Goals']['Daily']
    
    if w_excess > 0 and d_excess > 0:
        return "Weekly limit exceeded by " + str(w_excess) + "\n" + \
        "Daily limit exceeded by " + (d_excess) + "\n"
    elif d_excess > 0:
        return "Daily limit exceeded by " + (d_excess) + "\n"
    elif w_excess > 0: 
        return "Weekly limit exceeded by " + str(w_excess) + "\n"
    else:
        return "Daily Time = " + str(data[today_index]) + "\n" + \
        "Weekly Time = " + str(data['Tot']) + "\n" + \
        "No goals exceeded! Good job not procrastinating!" + "\n"

@app.route('/usage/<string:name>/', methods = ['PUT'])      
# curl -H "Content-type: application/json" -X PUT http://127.0.0.1:5000/usage/Byron/ -d '{"Instagram": 5}'

def takeJson(name):
    now = datetime.datetime.now()
    day = now.strftime("%a")            #gives current day of week abbrev
    today_index = dayToIndex(day)       #converts to day of week as referenced in the database
    doc = db.get(name)  
    jdata = json.loads(request.data)    #converts the incoming json request to a json dictionary
    
    for app in jdata:       
        if app not in doc:              #if not in 'Appdata', then insert the app by calling the App function before updating usage in database 
            App(name,app)
        index =  str(app)
        doc['Appdata'][index][today_index] = jdata[index] 

    db[name] = doc

    return "Hello " + str(jdata) + "\n"     #confimation that the json data was received
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    
