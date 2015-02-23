import time
from find import find
import database

# Contains algortithms for calculating average power consumption
class AverageAlgorithms:

    # Initialize the list to a empty list
    average = 0
    length = 0
    previousSendTime = 0
    sendInterval = 30

    def __init__(self):
        average = 0

    def updateAverage(self, points):
        f = lambda x: x[2]
        newSum = sum(map(f, points))
        totLen = self.length + len(points)
        self.average = ((self.average * self.length) + newSum) / totLen
        self.length = totLen

        print("times: "+str(points[0][0]) + " " + str(self.previousSendTime))
        if points[0][0] - self.previousSendTime > self.sendInterval:
            self.previousSendTime = points[0][0]
            print("send average")
            database.sendAverage(self.average)

        return self.average

    def getCurrentAverage(self):
        return self.average
