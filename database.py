from influxdb import InfluxDBClient
import json

global client

def fixData(data):
    baseStr=["time", "sequence_number", "power", "energy"]
    tmp=[]
    for i in range(len(data["points"])) :
        tmp=[]
        tmp.append(data["points"][i][data["columns"].index(baseStr[0])])
        tmp.append(data["points"][i][data["columns"].index(baseStr[1])])
        tmp.append(data["points"][i][data["columns"].index(baseStr[2])])
        tmp.append(data["points"][i][data["columns"].index(baseStr[3])])
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
    data=fixData(data)
    return data

# NOT IMPLEMENTED
def sendAverage(average):
    switchDatabase("grupp5")
    # points = ""
    json_body = "[{\"name\" : \"average_v1\",\"columns\" : [\"average\"],\"points\" : [[" + str(average) + "]]}]"
    client.write_points(json_body)
    result = client.query('select average from average_v1;')
    switchDatabase("Munktell")


def switchDatabase(name):
    client.switch_database(name)
