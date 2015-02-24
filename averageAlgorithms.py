import time
import datetime
from find import find
import database

def calcAverage(points):
    f = lambda x: x[3]
    newSum = sum(map(f, points))
    average = newSum / len(points)
    return average

def calculateAverageDay():
    d = datetime.date.today() - datetime.timedelta(hours=1)
    return fetchNCalc("averageHour", d)

def calculateAverageWeek():
    d = datetime.date.today() - datetime.timedelta(days=7)
    return fetchNCalc("averageDay", d)


def calculateAverageMonth():
    d = datetime.date.today() - datetime.timedelta(weeks=4)
    return fetchNCalc("averageWeek", d)

def fetchNCalc(id, time):
    now = time.strftime('%Y-%m-%d %H:%M:%S.000')
    query = "select * from \"events\" where id = \'" + id + "\' and time > \'" + now + "\';"
    data = database.requestEventData(query)
    return calcAverage(data["points"])

# Contains algortithms for calculating average power consumption
class AverageAlgorithms:

    # Initialize the list to a empty list
    average = 0
    length = 0

    def __init__(self):
        average = 0
        self.previousHour = datetime.datetime.now().second
        self.previousDay = datetime.datetime.now().day
        self.previousWeek = datetime.date.today().isocalendar()[1]
        self.previousMonth = datetime.datetime.now().month

    # fetchNCalc averages to database
    def sendAverages(self):
        currentTime = datetime.datetime.now()
        # fetchNCalc event to database if a hour has passed
        if currentTime.second != self.previousHour:
            self.previousHour = currentTime.second
            database.sendEvent("averageHour", self.average, 1)

        # fetchNCalc event to database if a day has passed
        if currentTime.day != self.previousDay:
            self.previousDay = currentTime.day
            averageDay = calculateAverageDay()
            database.sendEvent("averageDay", averageDay, 2)

        weekNumber = datetime.date.today().isocalendar()[1]
        # fetchNCalc event to database if a week has passed
        if weekNumber != self.previousWeek:
            self.previousWeek = weekNumber
            averageWeek = calculateAverageWeek()
            database.sendEvent("averageWeek", averageWeek, 3)

        # fetchNCalc event to database if a month has passed
        if currentTime.month != self.previousMonth:
            self.previousMonth = currentTime.month
            averageMonth = calculateAverageMonth()
            database.sendEvent("averageMonth", averageMonth, 4)


    def updateAverage(self, points):
        f = lambda x: x[2]
        newSum = sum(map(f, points))
        totLen = self.length + len(points)
        self.average = ((self.average * self.length) + newSum) / totLen
        self.length = totLen

        self.sendAverages()

        return self.average

    def getCurrentAverage(self):
        return self.average
