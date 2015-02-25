from influxdb import InfluxDBClient
import json
import threading
import time
import datetime
import database
from transitionAlgorithms import TransitionAlgorithms
from averageAlgorithms import AverageAlgorithms
from priorityFramework import PriorityFramework
import Algorithms

global lastTime
global transitionAlgorithms
global averageAlgorithms
global priorityFramework

# Start thread to run work every 60 seconds
def work ():
    check()
    threading.Timer(20, work).start()

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
    transitionAlgorithms.updatePoints(data["points"])
    average = averageAlgorithms.updateAverage(data["points"])
    priorityFramework.sendAverages(transitionAlgorithms.list)
    setTime(data)

# Initialize database variable, connect to database, send query to influxDB to set the current time
def init():
    global transitionAlgorithms
    global averageAlgorithms
    global priorityFramework
    transitionAlgorithms = TransitionAlgorithms()
    averageAlgorithms = AverageAlgorithms()
    priorityFramework = PriorityFramework()
    priorityFramework.addFunction(averageAlgorithms.calculateAverage, "long")
    priorityFramework.addFunction(transitionAlgorithms.lookForFastChange, "minute")
    priorityFramework.addFunction(transitionAlgorithms.lookForSlowChange, "minute")
    priorityFramework.addFunction(Algorithms.min, "long")
    priorityFramework.addFunction(Algorithms.max, "long")
    database.connectToDatabase()
    query = 'select * from "test1" limit 2;'
    data = database.requestData(query)
    setTime(data)


class Fetch:

    def start():
        init()
        work()
