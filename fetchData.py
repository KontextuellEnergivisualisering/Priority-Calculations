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

# Start thread to run the function work every 8 seconds
def work ():
    check()
    # Start the work function in 8 seconds
    threading.Timer(8, work).start()

# Set time when last point was fetched
def setTime(data):
    global lastTime
    # Time manipulation
    now = time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(data["points"][0][0]))
    date_object = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S.000')
    # Subtract the time with one hour because UTC (probably should use a function to convert from UTC, but you know ... short on time)
    lastTime = (date_object - datetime.timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S.000')

# Fetch all data from influxDB since 'lastTime' data were fetched
def check():
    # Get mainmeter data from influxDB
    query = 'select * from "test1" where time > \'' + lastTime + '\';'
    data = database.requestData(query)
    # Update with last fetched points
    transitionAlgorithms.updatePoints(data["points"])
    # Calculate priorities
    priorityFramework.updatePriority(transitionAlgorithms.list)
    # Set time when data were fetched
    setTime(data)

# Initialize database variable, connect to database, send query to influxDB to fetch last points and set the current time
def init():
    global transitionAlgorithms
    global averageAlgorithms
    global priorityFramework
    transitionAlgorithms = TransitionAlgorithms()
    averageAlgorithms = AverageAlgorithms()
    priorityFramework = PriorityFramework()
    # Add functions to run on a regular basis
    priorityFramework.addFunction(averageAlgorithms.calculateAverage, "long")
    priorityFramework.addFunction(transitionAlgorithms.lookForFastChange, "minute")
    priorityFramework.addFunction(transitionAlgorithms.lookForSlowChange, "minute")
    priorityFramework.addFunction(Algorithms.min, "long")
    priorityFramework.addFunction(Algorithms.max, "long")
    # Connect to influxDB
    database.connectToDatabase()
    # Create request query and send request to initialize the last time the database were updated
    query = 'select * from "test1" limit 2;'
    data = database.requestData(query)
    setTime(data)


class Fetch:
    # Start the data fetching and analysis
    def start():
        init()
        work()
