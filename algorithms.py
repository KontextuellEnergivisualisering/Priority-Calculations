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

    # Add 'points' to list and keeps the list under 1200 points and discard the oldest items
    def addToList(self, points):
        if len(points) > 1:
            points.pop()


        newList = points + self.list
        while len(newList) > 3600:
            newList.pop()

        self.list = newList

    # Check if there has been a change during the specified 'timeSpan'
    def checkForChange(self, timeSpan):
        index = find(self.list, self.list[0][0] - timeSpan)
        # print("find " + time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[index][0])))
        str1 = "".join(str(v)+" " for v in self.list[0])
        str2 = "".join(str(v)+" " for v in self.list[index])
        print("points = "+str1 + " | " + str2)
        change = (self.list[0][2] / self.list[index][2]) - 1
        print("ennergy change (%) = " + str(change * 100))


    def calculateHeightDiff(self, pointNow, pointOld):
        diff = pointNow[2] - pointOld[2]
        return diff

    # Get the current lists length
    def getLength(self):
        return len(self.list)

    # Returns the list
    def getList(self):
        return self.list
