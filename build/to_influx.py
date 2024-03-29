#!/usr/bin/python3

import sys
import json
import os
from influxdb import InfluxDBClient # apt-get install -y python3-influxdb

# Set this to 1 if we only want to write the sensors defined as env-variable
# to be written to db

drop_undefined_sensors = 0

# get ENV

dbsrv_1  = os.environ['INFLUX_SRV']

if os.environ['INFLUX_SRV2'] is not None:
	dbsrv_2 = os.environ['INFLUX_SRV2']

dbport = os.environ['INFLUX_PORT']
dbuser = os.environ['INFLUX_USER']
dbpw = os.environ['INFLUX_PW']
dbname = os.environ['INFLUX_NAME']

sys.argv.pop(0)
string_input = ''.join(sys.argv)

print("Got data: " + string_input)

json_input = json.loads(string_input)

# example-input from sensor
# {"time":"2019-11-2814:09:37","model":"Prologue-TH","subtype":5,"id":55,"channel":1,"battery_ok":1,"temperature_C":22.900,"button":0,"humidity":15}

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

# Find a unique name for the measurement

measurement_name = ""

if "model" in json_input:
	measurement_name = json_input["model"]

	# replace all hyphens as they are not allowed as environment variables
	measurement_name = measurement_name.replace('-', '_')
	json_input.pop("model")
else:
	measurement_name = "unkown_sensor"

if "subtype" in json_input:
	measurement_name = measurement_name + "_SUBTYPE" + str(json_input["subtype"])
	json_input.pop("subtype")

if "id" in json_input:
	measurement_name = measurement_name + "_ID" + str(json_input["id"])
	json_input.pop("id")

# Look up if there is a user-defined name for this sensor in the env-variables
# and use it as the name of the measurement.

# Example: export Prologue-TH_SUBTYPE9_ID33 = "livingroom"
 
if measurement_name in os.environ:
	print("This sensor is well-known as " + os.environ[measurement_name] + ".")
	tags["description"] = measurement_name
	measurement_name = os.environ[measurement_name]

# Stop here if we do not want to datamine the whole neighborship

elif drop_undefined_sensors:
	exit(0)

# extract metadata-tags

if "channel" in json_input:
	tags["channel"] = json_input["channel"]
	json_input.pop("channel")

if "flags" in json_input:
	tags["flags"] = json_input["flags"]
	json_input.pop("flags")

if "type" in json_input:
	tags["type"] = json_input["type"]
	json_input.pop("type")

if "code" in json_input:
	tags["code"] = json_input["code"]
	json_input.pop("code")

if "sid" in json_input:
	tags["sid"] = json_input["sid"]
	json_input.pop("sid")

if "transmit" in json_input:
	tags["code"] = json_input["transmit"]
	json_input.pop("transmit")

if "mic" in json_input:
	tags["mic"] = json_input["mic"]
	json_input.pop("mic")

# everything else should be measurement data
# if not, extract it here like the examples above

fields = json_input

json_body = [ { "measurement" : measurement_name, "tags" : tags, "fields" : fields  } ]

# write data

try:
	client = InfluxDBClient(dbsrv_1, dbport, dbuser, dbpw, dbname)
	client.write_points(json_body)
except:
	print("Error writing to " + dbsrv_1 + ":" + dbport + ".")

try:
	client = InfluxDBClient(dbsrv_2, dbport, dbuser, dbpw, dbname)
	client.write_points(json_body)
except:
	print("Error writing to " + dbsrv_1 + ":" + dbport + ".")

exit(0)
