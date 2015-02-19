from influxdb import InfluxDBClient
import json
import pdb
from find import findSampleDiff

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

        print(findSampleDiff(newList, 5))

    # Check if there has been a change during the specified 'timeSpan'
    def checkForChange(self, timeSpan):
        index = 0

    # Get the current lists length
    def getLength(self):
        return len(self.list)

    # Returns the list
    def getList(self):
        return self.list
