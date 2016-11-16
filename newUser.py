#!/usr/bin/env python

from flask import Flask, request
import couchdb, json, datetime
app = Flask(__name__)

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
    return "Welcome to RMP"

@app.route('/view/', methods = ['GET'])
def getDocs():
    #curl -X GET http://localhost:5000/view/    
    return json.dumps(db.get('_all_docs')) + "\n"

@app.route('/get/<string:name>/', methods = ['GET'])
def getName(name):
    #curl -X PUT http://localhost:5000/get/<name>    
    if name in db:
        return json.dumps(db.get(name)) + "\n"
    else:
        return "User not in database"

@app.route('/newuser/<string:name>/', methods = ['PUT'])
def newUser(name):
    db[name] = {'name': name, 'Appdata': {'Total': Weekly}, 'Goals': Goals}
    if name in db:
        return "Successfully inserted " + name + "\n"
    else:
        return "Failed to insert"
    

@app.route('/app/<string:name>/<string:app>/', methods = ['PUT','DELETE'])

def App(name,app): 
    doc = db.get(name)
    if request.method == "PUT":
        if app in doc['Appdata']:
            return app + " already in Appdata" + "\n"
        else:
            doc['Appdata'][app] = Weekly
            db[name] = doc
            return "Successfully inserted " + app + "\n" 
    elif request.method == "DELETE":
        if app in doc['Appdata']:
            del doc['Appdata'][app]
            db[name] = doc
            return "Successfully deleted " + app + "\n"
        else:
            return app + " not in Appdata" + "\n"



@app.route('/goal/<string:name>/<int:daily>/<int:weekly>/', methods = ['GET', 'PUT'])
def newGoal(name,daily,weekly):
    doc = db.get(name)
    doc['Goals']['Daily'] = daily 
    doc['Goals']['Weekly'] = weekly
    db[name] = doc
    return "New Daily is: " + str(daily) + "\n" + "New Weekly is: " + str(weekly) + "\n"
    
@app.route('/compare/<string:name>/', methods = ['GET'])
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
        "No goals exceeded! Good job not procrastinating!" + "\n" + \
        today_index + str(doc['Goals']['Weekly']) + "\n"


    

if __name__ == '__main__':
    app.debug = True
    app.run()
    
