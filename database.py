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
    client = InfluxDBClient(host, port, user, password, dbname)

# Send request to influxDB to fetch data corresponding to the query 'query'
def requestData(query):
    result = client.query(query)
    str2 = "".join(str(v) for v in result)
    str2 = str2.replace("'","\"")
    data = json.loads(str2)
    data = fixDataGen(data, ["time", "sequence_number", "power", "energy"])
    return data

def requestEventData(query):
    switchDatabase("grupp5")
    result = client.query(query)
    switchDatabase("Munktell")
    str2 = "".join(str(v) for v in result)
    str2 = str2.replace("'","\"")
    data = json.loads(str2)
    data = fixDataGen(data, ["time", "sequence_number", "value", "id", "priority"])
    return data

def sendMultipleEvent(list):
    switchDatabase("grupp5")
    points = ""
    print("--------------------------------------")
    for item in list:
        a = "[" + str(item[0]) + ", \"" + item[1] + "\", " + str(item[2]) + "],"
        print(a)
        points += a

    # print("--------------------------------------")
    points = points[:-1]
    json_body = "[{\"name\" : \"events\",\"columns\" : [\"value\", \"id\", \"priority\"],\"points\" : [" + points + "]}]"
    # print("write: " + json_body)
    client.write_points(json_body)
    switchDatabase("Munktell")


def switchDatabase(name):
    client.switch_database(name)
