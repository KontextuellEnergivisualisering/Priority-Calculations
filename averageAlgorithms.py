# Contains algortithms for calculating average power consumption
class AverageAlgorithms:

    # Calculates the power based on the points, the 'lastHourData' is not used
    def calculateAverage(self, points, lastHourData):
        f = lambda x: x[2]
        newSum = sum(map(f, points))
        average = newSum / len(points)
        return [average, "average", 2, time.gmtime(0)]
