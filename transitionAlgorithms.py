import time
from find import find
import statistics

# Contains algortithms for detecting change in data points
class TransitionAlgorithms:

    # Initialize the power list to a empty list
    list = []
    slowThreshold = 3                 # Threshold for power change when slow transition
    fastThreshold = 6                 # Threshold for power change when fast transition
    stableTime = 5                    # Minimum time to determine if power change is stable
    fastTime = 40                     # Minimum time to determine if power change is fast
    slowTime = 1800                   # Minimum time to determine if power change is slow
    fastChangeFound = 0               # Time when a fast power transtion occured
    slowChangeFound = 0               # Time when a slow power transtion occured

    # Does things connected to updating points
    def updatePoints(self, points):
        self.list = self.keepListUpdated(points)

    # Makes sure the points are less than 3600, if not less it removes the oldest points until number of points are less than 3600
    def keepListUpdated(self, points):
        # Remove the last item because the data fetches the first item in previous query twice
        if len(points) > 1:
            points.pop()

        # Concatenate new points with old points and keep number of points less than 3600
        newList = points + self.list
        while len(newList) > 3600:
            newList.pop()

        return newList

    # Searches through the points to detect when a quick change in power occurs
    def lookForFastChange(self, points, lastHourData):
        # If it's long enough time since the last change was found look for another
        if lastHourData[0][0] > self.fastChangeFound:
            tup = self.lookForChange(self.stableTime, self.fastTime, lastHourData, self.fastThreshold)
            powerChange = tup["change"]
            time = tup["time"]
            if powerChange != 0:
                self.fastChangeFound = lastHourData[0][0] + self.fastTime
                return [powerChange, "fastTransition", 1, time]

    # Searches through the points to detect when a slow change in power occurs
    def lookForSlowChange(self, points, lastHourData):
        # If it's long enough time since the last change was found look for another
        if lastHourData[0][0] > self.slowChangeFound:
            tup = self.lookForChange(self.stableTime, self.slowTime, lastHourData, self.slowThreshold)
            powerChange = tup["change"]
            time = tup["time"]
            if powerChange != 0:
                self.slowChangeFound = lastHourData[0][0] + self.slowTime
                return [powerChange, "slowTransition", 1, time]

    # Determines if a change in power has occured, based on the two time parameters
    def lookForChange(self, shortTime, longTime, lastHourData, threshold):
        # Check for change in a small time span
        tup1 = self.checkForChange(shortTime, lastHourData)
        shortChange = tup1["change"]
        # Check for change in a long time span
        tup = self.checkForChange(longTime, lastHourData)
        longChange = tup["change"]
        index = tup["index"]
        # Calculate the ratio between the short time span and long timespan
        diff = longChange / shortChange
        print("difference: " + str(diff))
        if (diff >= threshold):
            # Return the maximum difference in power (negative or positive)
            return self.calculateMaxDiff(lastHourData, index)
        else:
            return {"change": 0, "time": 0}

    # Examine the standard deviation between now and a point 'timespan' seconds away
    def checkForChange(self, timeSpan, points):
        # Find the index of the element whose time is the current time (self.list[0][0]) subtracted with the specified timespan
        index = find(points, points[0][0] - timeSpan)
        # Calculate the difference between the two points to get the change in power
        change = self.calculateStdev(points, index)
        return {"change":change, "index":index}

    # Calculate the standard deviation in range '0' to 'index'
    def calculateStdev(self, points, index):
        if index < 2:
            return 0.0001

        p = points[:index]
        f = lambda x: x[2]
        p2 = map(f, p)
        return statistics.stdev(p2)


    # Calculate the maximum difference in power between two points (negative or positive)
    def calculateMaxDiff(self, points, index):
        p = points[:index]
        maxi = 0
        maxIndex=0
        for i in p:
            if abs(p[0][2]-i[2]) > abs(maxi):
                maxi = p[0][2]-i[2]
                maxIndex = i

        return {"change": maxi, "time": maxIndex[0]}
