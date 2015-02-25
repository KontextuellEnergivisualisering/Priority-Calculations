import time
import datetime
from find import find
import database

# Run every function in 'listOfFunctions' and store their response (if not empty response) in a list
def calculateForMinute(listOfFunctions, data):
    eventPoints = []
    postFix = "Minute"
    for funct in listOfFunctions:
        info = funct(data, data)
        if(info != [] and info != None):
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

# Run every function in 'listOfFunctions' and store their response (if not empty response) in a list
def calculateForHour(listOfFunctions, lastHourData):
    eventPoints = []
    postFix = "Hour"
    for funct in listOfFunctions:
        info = funct(lastHourData, lastHourData)
        if(info != [] and info != None):
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

# Run every function in 'listOfFunctions' and store their response (if not empty response) in a list
def calculateForDay(listOfFunctions, lastHourData):
    d = datetime.date.today() - datetime.timedelta(hours=1)
    return fetchNCalc("Hour", d, listOfFunctions, "Day", lastHourData)

# Run every function in 'listOfFunctions' and store their response (if not empty response) in a list
def calculateForWeek(listOfFunctions, lastHourData):
    d = datetime.date.today() - datetime.timedelta(days=7)
    return fetchNCalc("Day", d, listOfFunctions, "Week", lastHourData)

# Run every function in 'listOfFunctions' and store their response (if not empty response) in a list
def calculateForMonth(listOfFunctions, lastHourData):
    d = datetime.date.today() - datetime.timedelta(weeks=4)
    return fetchNCalc("Week", d, listOfFunctions, "Month", lastHourData)

# Run every function with specified arguments based on data from database
def fetchNCalc(id, time, listOfFunctions, postFix, lastHourData):
    now = time.strftime('%Y-%m-%d %H:%M:%S.000')
    query = "select * from \"events\" where id = \'" + id + "\' and time > \'" + now + "\';"
    data = database.requestEventData(query)
    eventPoints = []
    for funct in listOfFunctions:
        # Run function with arguments
        info = funct(data["points"], lastHourData)
        if (info != [] and info != None):
            # Add a postfix (suffix) to the end of id
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

# Contains framework for priorities
class PriorityFramework:

  def __init__(self):
    #   save the last time the program uploads data to database, different time intervals
      self.previousMinute = datetime.datetime.now().minute
      self.previousHour = datetime.datetime.now().hour
      self.previousDay = datetime.datetime.now().day
      self.previousWeek = datetime.date.today().isocalendar()[1]
      self.previousMonth = datetime.datetime.now().month
    #   List containing the functions to be run after a specified time interval
      self.runEveryMinuteFunctions = []
      self.runLessOftenFunctions = []

    # Add functions to be run based on a specific time interval, either run every minute, or every hour, day, week and month
    def addFunction(self, f, type):
        if type == "minute":
            self.runEveryMinuteFunctions.append(f)
        else:
            self.runLessOftenFunctions.append(f)

  # Do priority based calculations baed on different time intervals
  def updatePriority(self, lastHourData):
      currentTime = datetime.datetime.now()
      # send events to database if a minute has passed
      if currentTime.minute != self.previousMinute:
          self.previousMinute = currentTime.minute
          res = calculateForMinute(self.runEveryMinuteFunctions, lastHourData)
          database.sendMultipleEvent(res)

      # send events to database if a hour has passed
      if currentTime.hour != self.previousHour:
          self.previousHour = currentTime.hour
          res = calculateForHour(self.runLessOftenFunctions, lastHourData)
          database.sendMultipleEvent(res)

      # send events to database if a day has passed
      if currentTime.day != self.previousDay:
          self.previousDay = currentTime.day
          res = calculateForDay(self.runLessOftenFunctions, lastHourData)
          database.sendMultipleEvent(res)

      weekNumber = datetime.date.today().isocalendar()[1]
      # send events to database if a week has passed
      if weekNumber != self.previousWeek:
          self.previousWeek = weekNumber
          res = calculateForWeek(self.runLessOftenFunctions, lastHourData)
          database.sendMultipleEvent(res)

      # send events to database if a month has passed
      if currentTime.month != self.previousMonth:
          self.previousMonth = currentTime.month
          res = calculateForMonth(self.runLessOftenFunctions)
          database.sendMultipleEvent(res)
