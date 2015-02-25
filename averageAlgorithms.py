import time
import datetime
from find import find
import database

# Contains algortithms for calculating average power consumption
class AverageAlgorithms:

    average = 0
    length = 0

    def __init__(self):
        average = 0

    # Calculates the power based on the points, the 'lastHourData' is not used
    def calculateAverage(self, points, lastHourData):
        f = lambda x: x[2]
        newSum = sum(map(f, points))
        average = newSum / len(points)
        return [average, "average", 2]

    # Updates the current average
    def updateAverage(self, points):
        f = lambda x: x[2]
        newSum = sum(map(f, points))
        totLen = self.length + len(points)
        self.average = ((self.average * self.length) + newSum) / totLen
        self.length = totLen

        return self.average

    def getCurrentAverage(self):
        return self.average
