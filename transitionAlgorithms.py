import time
from find import find

# Contains algortithms for detecting change in data points
class TransitionAlgorithms:

    # Initialize the list to a empty list
    list = []
    stableThreshold = 0.01     # Threshold for power change when stable
    slowThreshold = 0.02        # Threshold for power change when slow transition
    fastThreshold = 0.03        # Threshold for power change when fast transition
    stableTime = 3              # Minimum time to determine if power change is stable
    fastTime = 7               # Minimum time to determine if power change is fast
    slowTime = 30               # Minimum time to determine if power change is slow
    fastChangeFound = 0
    slowChangeFound = 0

    def __init__(self):
        index = 0

    # Add 'points' to list and keeps the list under 1200 points and discard the oldest items
    def updatePoints(self, points):
        self.list = self.keepListUpdated(points)

    # Makes sure the points are less then 3600, if not less it removes points until number of points are less then 3600
    def keepListUpdated(self, points):
        if len(points) > 1:
            points.pop()

        # Concatenate new points with old points
        newList = points + self.list
        while len(newList) > 3600:
            newList.pop()

        return newList

    def lookForFastChange(self, points, lastHourData):
        if lastHourData[0][0] > self.fastChangeFound:
            powerChange = self.lookForChange(self.stableTime, self.fastTime, lastHourData)
            if powerChange != 0:
                self.fastChangeFound = lastHourData[0][0] + self.fastTime
                return [powerChange, "fastTransition", 1]

    def lookForSlowChange(self, points, lastHourData):
        if lastHourData[0][0] > self.slowChangeFound:
            powerChange = self.lookForChange(self.stableTime, self.slowTime, lastHourData)
            if powerChange != 0:
                self.slowChangeFound = lastHourData[0][0] + self.slowTime
                return [powerChange, "slowTransition", 1]

    # Determine if a change in power has occured
    def lookForChange(self, shortTime, longTime, lastHourData):
        tup1 = self.checkForChange(shortTime, lastHourData)
        shortChange = tup1["change"]
        tup = self.checkForChange(longTime, lastHourData)
        longChange = tup["change"]
        index = tup["index"]
        if (abs(shortChange) <= self.stableThreshold and abs(longChange) >= self.fastThreshold):
            return self.calculateHeightDiff(lastHourData[0], lastHourData[index])
        else:
            return 0

    # Check if there has been a change during the specified 'timeSpan' in seconds
    def checkForChange(self, timeSpan, points):
        # Find the index of the element whose time is the current time (self.list[0][0]) subtracted with the specified timespan
        index = find(points, points[0][0] - timeSpan)
        # Calculate the difference between the two points to get the change in power
        change = (points[0][2] / points[index][2]) - 1
        return {"change":change, "index":index}

    # Calculate the difference in power between two points
    def calculateHeightDiff(self, pointNow, pointOld):
        diff = pointNow[2] - pointOld[2]
        return diff

    # Get the current lists length
    def getLength(self):
        return len(self.list)

    # Returns the list
    def getList(self):
        return self.list
