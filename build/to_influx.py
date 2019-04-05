#!/usr/bin/python3

import sys
import json
import os
from influxdb import InfluxDBClient # apt-get install -y python3-influxdb

# get ENV

dbsrv = os.environ['INFLUX_SRV']
dbport = os.environ['INFLUX_PORT']
dbuser = os.environ['INFLUX_USER']
dbpw = os.environ['INFLUX_PW']
dbname = os.environ['INFLUX_NAME']

sys.argv.pop(0)
string_input = ''.join(sys.argv)

print("Got data: " + string_input)

json_input = json.loads(string_input)

# example-input from sensor
# {'time': '2019-04-0316:45:06', 'model': 'LaCrosse-TX', 'id': 125, 'temperature_C': 19.3}

# example-json for InfluxDB
# json_body = [
#        {
#            "measurement": "cpu_load_short",
#            "tags": {
#                "host": "server01",
#                "region": "us-west"
#            },
#            "time": "2009-11-10T23:00:00Z",
#            "fields": {
#                "Float_value": 0.64,
#                "Int_value": 3,
#                "String_value": "Text",
#                "Bool_value": True
#            }
#       }
# ]

json_body = []
tags = {}

# we don't use the time from the sensor, InfluxDB will set it according to its clock
json_input.pop("time")

# if there is an environment-variable for this sensor, tag the entry with a sensor-description
# example:
# export SENSOR_LaCrosseTXSensor_125 = "garden"

if "id" in json_input and "model" in json_input and "SENSOR_" + json_input["model"] + "_" + str(json_input["id"]) in os.environ:
    print("This sensor is well-known.")
    tags["description"] = os.environ["SENSOR_" + json_input["model"] + "_" + str(json_input["id"])]

# name of the measurement

measurement_name = "sensor-"

if "model" in json_input and json_input["model"] != "":
    measurement_name = measurement_name + json_input["model"]
    json_input.pop("model")
else:
    measurement_name = measurement-name + "unknown_type-"
    if "id" in json_input:
        measurement_name = measurement-name + str(json_input("id"))

if "id" in json_input:
    tags["id"] = json_input["id"]
    json_input.pop("id")

if "channel" in json_input:
    tags["channel"] = json_input["channel"]
    json_input.pop("channel")

# everything else should be measurement data
fields = json_input

json_body = [ { "measurement" : measurement_name, "tags" : tags, "fields" : fields  } ]

# write data

try:
    client = InfluxDBClient(dbsrv, dbport, dbuser, dbpw, dbname)
    client.write_points(json_body)
except:
    print("Error writing to " + dbsrv + ":" + dbport + ".")

exit(0)
