import time
from find import find

global client

# Contains algortithms for detecting change in data points
class Algorithms:

    # Initialize the list to a empty list
    list = []
    stableThreshold = 0.005
    slowThreshold = 0.02
    fastThreshold = 0.01
    stableTime = 5
    fastTime = 10
    slowTime = 30
    fastChangeFound = 0
    slowChangeFound = 0

    def __init__(self):
        index = 0

    # Add 'points' to list and keeps the list under 1200 points and discard the oldest items
    def updatePoints(self, points):

        self.list = self.keepListUpdated(points)
        print("----------------- Fast change --------------------")
        res = self.lookForFastChange()
        if res != 1:
            print("----------------- Slow change --------------------")
            self.lookForSlowChange()
            # print("-------------------------------------")

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
        # str1 = "".join(str(v)+" " for v in self.list[0])
        # str2 = "".join(str(v)+" " for v in self.list[index])
        # print("points = "+str1 + " | " + str2)
        # Calculate the difference between the two points to get the change in power
        change = (self.list[0][2] / self.list[index][2]) - 1
        print("ennergy change (%) = " + str(round(change * 100, 2)))
        return {"change":change, "index":index}

    # Check if data points indicate a fast transition in power
    def lookForFastChange(self):
        if self.list[0][0] > self.fastChangeFound:
            powerChange = self.lookForChange(self.stableTime, self.fastTime)
            if powerChange != 0:
                self.fastChangeFound = self.list[0][0] + self.fastTime
                print("Found a FAST transition at time: " + str(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[0][0]))))
                print("Power difference = " + str(powerChange))

    # Check if data points indicate a slow transition in power
    def lookForSlowChange(self):
        if self.list[0][0] > self.slowChangeFound:
            powerChange = self.lookForChange(self.stableTime, self.slowTime)
            if powerChange != 0:
                self.slowChangeFound = self.list[0][0] + self.slowTime
                print("Found a SLOW transition at time: " + str(time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(self.list[0][0]))))
                print("Power difference = " + str(powerChange))

    def lookForChange(self, shortTime, longTime):
        tup1 = self.checkForChange(shortTime)
        shortChange = tup1["change"]
        tup = self.checkForChange(longTime)
        longChange = tup["change"]
        index = tup["index"]
        print(str(abs(shortChange)) +" <= "+str(self.stableThreshold) + " && " + str(abs(longChange))+" >= "+str(self.fastThreshold))
        if (abs(shortChange) <= self.stableThreshold and abs(longChange) >= self.fastThreshold):
            return self.calculateHeightDiff(self.list[0], self.list[index])
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
