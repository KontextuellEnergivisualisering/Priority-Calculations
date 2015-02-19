from influxdb import InfluxDBClient
import json
import threading
import time
import datetime
from database import Database
from algorithms import Algorithms


global lastTime
global database
global algorithms

# Start thread to run work every 60 seconds
def work ():
    check()
    threading.Timer(5, work).start()

# Print sequence_number from points to determine if data is fetchd in the correct order
def analysePoints(data):

   for s in reversed(data):
       print(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(s[0])))

# Set time when last point was fetched
def setTime(data):
    global lastTime
    now = time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(data["points"][0][0]))
    date_object = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S.000')
    # Subtract the time with one hour because reasons
    lastTime = (date_object - datetime.timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S.000')

# Fetch all data from influxDB since 'lastTime' data were fetched
def check():
    query = 'select * from "test1" where time > \'' + lastTime + '\';'
    data = database.requestData(query)
    algorithms.addToList(data["points"])
    print(algorithms.getLength())
    print("-----------------------------------------")
    analysePoints(algorithms.getList())
    print("-----------------------------------------")
    setTime(data)

# Initialize database variable, connect to database, send query to influxDB to set the current time
def init():
    global database
    global algorithms
    database = Database()
    algorithms = Algorithms()
    database.connectToDatabase()
    query = 'select * from "test1" limit 2;'
    data = database.requestData(query)
    setTime(data)


class Fetch:

    def start():
        init()
        work()
