import time
import datetime
from find import find
import database

def calculateForMinute(list, data):
    eventPoints = []
    postFix = "Minute"
    for funct in list:
        info = funct(data, data)
        if(info != [] and info != None):
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

def calculateForHour(list, data):
    eventPoints = []
    postFix = "Hour"
    for funct in list:
        info = funct(data, data)
        if(info != [] and info != None):
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

def calculateForDay(list, lastHourData):
    d = datetime.date.today() - datetime.timedelta(hours=1)
    return fetchNCalc("Hour", d, list, "Day", lastHourData)

def calculateForWeek(list, lastHourData):
    d = datetime.date.today() - datetime.timedelta(days=7)
    return fetchNCalc("Day", d, list, "Week", lastHourData)

def calculateForMonth(list, lastHourData):
    d = datetime.date.today() - datetime.timedelta(weeks=4)
    return fetchNCalc("Week", d, list, "Month", lastHourData)

def fetchNCalc(id, time, list, postFix, lastHourData):
    now = time.strftime('%Y-%m-%d %H:%M:%S.000')
    query = "select * from \"events\" where id = \'" + id + "\' and time > \'" + now + "\';"
    data = database.requestEventData(query)
    eventPoints = []
    for funct in list:
        info = funct(data["points"], lastHourData)
        if (info != [] and info != None):
            info[1] += postFix
            eventPoints.append(info)
    return eventPoints

# Contains framework for
class SendFramework:

  def __init__(self):
      self.previousMinute = datetime.datetime.now().minute
      self.previousHour = datetime.datetime.now().hour
      self.previousDay = datetime.datetime.now().day
      self.previousWeek = datetime.date.today().isocalendar()[1]
      self.previousMonth = datetime.datetime.now().month
      self.funMinuteList = []
      self.funLongList = []

  def addFunction(self, f, type):
        if type == "minute":
            self.funMinuteList.append(f)
        else:
            self.funLongList.append(f)

  # send averages to database
  def updatePriority(self, lastHourData):
      currentTime = datetime.datetime.now()
      # send event to database if a hour has passed

      if currentTime.minute != self.previousMinute:
          self.previousMinute = currentTime.minute
          res = calculateForMinute(self.funMinuteList, lastHourData)
          database.sendMultipleEvent(res)

      if currentTime.hour != self.previousHour:
          self.previousHour = currentTime.hour
          res = calculateForHour(self.funLongList, lastHourData)
          database.sendMultipleEvent(res)

      # send event to database if a day has passed
      if currentTime.day != self.previousDay:
          self.previousDay = currentTime.day
          res = calculateForDay(self.funLongList, lastHourData)
          database.sendMultipleEvent(res)

      weekNumber = datetime.date.today().isocalendar()[1]
      # send event to database if a week has passed
      if weekNumber != self.previousWeek:
          self.previousWeek = weekNumber
          res = calculateForWeek(self.funLongList, lastHourData)
          database.sendMultipleEvent(res)

      # send event to database if a month has passed
      if currentTime.month != self.previousMonth:
          self.previousMonth = currentTime.month
          res = calculateForMonth(self.funLongList)
          database.sendMultipleEvent(res)
