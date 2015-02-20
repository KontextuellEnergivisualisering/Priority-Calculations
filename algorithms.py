from influxdb import InfluxDBClient
import json
import pdb
import time
from find import find

global client

# Contains algortithms for detecting change in data points
class Algorithms:
    # Initialize the list to a empty list
    def __init__(self):
        self.list = []
        self.stableThreshold = 0.5
        self.slowThreshold = 2
        self.fastThreshold = 1

    # Add 'points' to list and keeps the list under 1200 points and discard the oldest items
    def updatePoints(self, points):

        self.list = self.keepListUpdated(points)
        res = self.lookForFastChange()
        if res != 1:
            self.lookForSlowChange()

    def keepListUpdated(self, points):
        if len(points) > 1:
            points.pop()


        newList = points + self.list
        while len(newList) > 3600:
            newList.pop()

        return newList

    # Check if there has been a change during the specified 'timeSpan' in seconds
    def checkForChange(self, timeSpan):
        # Find the index of the element whose time is the current time (self.list[0][0]) subtracted with the specified timespan
        index = find(self.list, self.list[0][0] - timeSpan)
        # print("find " + time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[index][0])))
        # TEST OUTPUT CODE FOR THE POINT DATA
        str1 = "".join(str(v)+" " for v in self.list[0])
        str2 = "".join(str(v)+" " for v in self.list[index])
        print("points = "+str1 + " | " + str2)
        # Calculate the difference between the two points to get the change in power
        change = (self.list[0][2] / self.list[index][2]) - 1
        print("ennergy change (%) = " + str(round(change * 100, 2)))
        return change

    # Check if data points indicate a fast transition in power
    def lookForFastChange(self):
        hasChanged = self.lookForChange(5, 10)
        if hasChanged == 1:
            print("Found a FAST transition at time: " + str(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[0][0]))))

    # Check if data points indicate a slow transition in power
    def lookForSlowChange(self):
        hasChanged = self.lookForChange(5, 30)
        if hasChanged == 1:
            print("Found a SLOW transition at time: " + str(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[0][0]))))

    def lookForChange(self, shortTime, longTime):
        shortChange = self.checkForChange(shortTime)
        longChange = self.checkForChange(longTime)
        if (abs(shortChange) <= self.stableThreshold and abs(longChange) >= self.fastThreshold):
            return 1
        else:
            return 0

    def calculateHeightDiff(self, pointNow, pointOld):
        diff = pointNow[2] - pointOld[2]
        return diff

    # Get the current lists length
    def getLength(self):
        return len(self.list)

    # Returns the list
    def getList(self):
        return self.list
