from influxdb import InfluxDBClient
import json

class database:

    client

    def connectToDatabase():
        host = 'localhost'
        port = 8086
        user = 'root'
        password = 'root'
        dbname = 'Munktell'
        dbuser = 'grupp5-context'
        dbuser_password = 'grupp5'
        query = 'select * from "test1" limit 5;'
        client = InfluxDBClient(host, port, user, password, dbname)
        return client

    def requestData(query):
        global client
        result = client.query(query)
        str2 = "".join(str(v) for v in result)
        str2 = str2.replace("'","\"")
        # print("Result: {0}".format(str2))
        data = json.loads(str2)
        return data

    def sendPoints(data):
        points = ""
        json_body = "[{\"name\" : \"log_lines\",\"columns\" : [\"line\"],\"points\" : [[\"here's some useful log info from paul@influxdb.com\"]]}]"
        for s in data2:
            points = points + s[2]

        # print("Result: {0}".format(points))
        client.write_points(json_body)
        result = client.query('select line from log_lines;')

    def switchDatabase():
