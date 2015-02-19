from influxdb import InfluxDBClient
import json

class Database:

    def __init__(self):
        self.client = None

    # Connect to 'Munktell' database hosted on influxDB
    def connectToDatabase(self):
        host = 'localhost'
        port = 8086
        user = 'root'
        password = 'root'
        dbname = 'Munktell'
        dbuser = 'grupp5-context'
        dbuser_password = 'grupp5'
        query = 'select * from "test1" limit 5;'
        self.client = InfluxDBClient(host, port, user, password, dbname)

    # Send request to influxDB to fetch data corresponding to the query 'query'
    def requestData(self, query):
        result = self.client.query(query)
        str2 = "".join(str(v) for v in result)
        str2 = str2.replace("'","\"")
        data = json.loads(str2)
        return data

    # NOT IMPLEMENTED
    def sendPoints(self, data):
        points = ""
        json_body = "[{\"name\" : \"log_lines\",\"columns\" : [\"line\"],\"points\" : [[\"here's some useful log info from paul@influxdb.com\"]]}]"
        for s in data2:
            points = points + s[2]

        client.write_points(json_body)
        result = self.client.query('select line from log_lines;')

    # NOT IMPLEMENTED
    def switchDatabase():
        result = 0
