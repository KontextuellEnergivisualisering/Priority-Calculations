from influxdb import InfluxDBClient
import json

global client

def fixDataGen(data, baseStr):
    tmp=[]
    for i in range(len(data["points"])) :
        tmp=[]
        for st in baseStr:
            tmp.append(data["points"][i][data["columns"].index(st)])

        data["points"][i] = tmp

    return data

# Connect to 'Munktell' database hosted on influxDB
def connectToDatabase():
    global client
    host = 'localhost'
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'Munktell'
    dbuser = 'grupp5-context'
    dbuser_password = 'grupp5'
    query = 'select * from "test1" limit 5;'
    client = InfluxDBClient(host, port, user, password, dbname)

# Send request to influxDB to fetch data corresponding to the query 'query'
def requestData(query):
    result = client.query(query)
    str2 = "".join(str(v) for v in result)
    str2 = str2.replace("'","\"")
    # print("Result: " + str2)
    data = json.loads(str2)
    data = fixDataGen(data, ["time", "sequence_number", "power", "energy"])
    return data

def requestEventData(query):
    switchDatabase("grupp5")
    result = client.query(query)
    switchDatabase("Munktell")
    str2 = "".join(str(v) for v in result)
    str2 = str2.replace("'","\"")
    # print("Result: " + str2)
    data = json.loads(str2)
    data = fixDataGen(data, ["time", "sequence_number", "id", "value", "priority"])
    return data

# NOT IMPLEMENTED
def sendEvent(id, value, priority):
    switchDatabase("grupp5")
    json_body = "[{\"name\" : \"events\",\"columns\" : [\"id\", \"value\", \"priority\"],\"points\" : [[\"" + id + "\", " + str(value) + ", " + str(priority) + "]]}]"
    client.write_points(json_body)
    # result = client.query('select average from average_v1;')
    # str2 = "".join(str(v) for v in result)
    # str2 = str2.replace("'","\"")
    # print("Result from average_v1: " + str2)
    switchDatabase("Munktell")


def switchDatabase(name):
    client.switch_database(name)
