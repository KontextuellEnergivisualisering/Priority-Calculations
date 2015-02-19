from influxdb import InfluxDBClient
import json
import pdb

global client

# NOT IMPLMENTED
class Algorithms:

    def __init__(self):
        self.list = None

    def addToList(self, points):
        newList = points + self.list
        while len(newList) > 1200
            newList.pop()

        self.list = newList
