from influxdb import InfluxDBClient
import json
import pdb

global client

# NOT IMPLMENTED
class Algorithms:

    def __init__(self):
        self.list = []

    def addToList(self, points):
        if len(points) > 1: 
            points.pop()


        newList = points + self.list
        while len(newList) > 10:
            newList.pop()

        self.list = newList

    def getLength(self):
        return len(self.list)

    def getList(self):
        return self.list
