from influxdb import InfluxDBClient
import json

# Database client
global client

# Order data in a specific order specified by baseStr
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
    # Convert the data to a string
    str2 = "".join(str(v) for v in result)
    # Replace " with '
    str2 = str2.replace("'","\"")
    # Convert the string to a JSON object
    data = json.loads(str2)
    # Order data in a specific order
    data = fixDataGen(data, ["time", "sequence_number", "power", "energy"])
    return data

# Request data from the 'grupp5' serie
def requestEventData(query):
    # Switch database to 'grupp5'
    switchDatabase("grupp5")
    result = client.query(query)
    # Switch database to 'Munktell'
    switchDatabase("Munktell")
    # Convert the data to a string
    str2 = "".join(str(v) for v in result)
    # Replace " with '
    str2 = str2.replace("'","\"")
    # Convert the string to a JSON object
    data = json.loads(str2)
    # Order data in a specific order
    data = fixDataGen(data, ["time", "sequence_number", "value", "id", "priority"])
    return data

# Send all points specified in 'list' to database
def sendMultipleEvent(list):
    switchDatabase("grupp5")
    points = ""
    print("--------------------------------------")
    # Format and concatinate all points from list
    for item in list:
        a = "[" + str(item[0]) + ", \"" + item[1] + "\", " + str(item[2]) + ", "+str(item[3])+"],"
        points += a
        # Print the formated string for logging purpose
        print(a)

    # Remove last character (',')
    points = points[:-1]
    json_body = "[{\"name\" : \"events\",\"columns\" : [\"value\", \"id\", \"priority\", \"time\"],\"points\" : [" + points + "]}]"
    # Send points to influxDB
    client.write_points(json_body)
    switchDatabase("Munktell")


def switchDatabase(name):
    client.switch_database(name)
