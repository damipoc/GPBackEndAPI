"""

Currently receives data from hardware in following format:
{
    "ts":"timestamp",
    "data":[
        {
            "name":"string",
            "reading":"value"
        }
    ]
}

Checks if data and timestamp is received and echoes back the proccess in the command window
If timestamp is not showing, it is assigned server one and if name or reading is missing then it doesn't accept the post request
Current endpoint is http://localhost:5000/devices/<device>/telemetry with <devices> being replaced by the device ID
For testing purposes once everything goes well it displays the data posted both on command window and endpoint

"""


import datetime
from datetime import datetime
from databaseAccess import DatabaseAccess
from flask import request, jsonify, Blueprint

backend_api = Blueprint("backend_api", __name__)


@backend_api.route('/devices/<device>/telemetry', methods=['POST'])
def post_device_telemetry(device):

    # Accessing database
    dbAccess = DatabaseAccess()

    # If device not on list return 401
    if not dbAccess.device_exists(device):
        return 401

    # Receiving request
    tele_data = request.get_json()

    # Assigning received data
    tele_name = tele_data['data'][0]['name']
    tele_reading = str(tele_data['data'][0]['reading'])

    # if no timestamp is received assign epoch server time
    if not tele_data['ts']:
        tele_timestamp = datetime.utcnow().timestamp()
        print("No timestamp received, assigning server")
    else:
        tele_timestamp = tele_data['ts']

    # If no name or reading received, do not accept
    if not tele_reading:
        print("No reading, discarding")
        return ""
    elif not tele_name:
        print("No name, discarding")
        return ""

    # Echoes data received
    print("Data received, Device:" + str(device) + " Time: " + str(tele_timestamp) + " Name: " + str(tele_name) + " Reading: " + str(tele_reading))

    # Formats the data for the database
    tele_valid_data = jsonify({device: {'ts': tele_timestamp, 'data': [tele_data['data'][0]]}})

    # Anomaly Detect
    print("Sending to anomaly detection.")
    anomaly_detect()

    # Database, sql error for now
    print("Sending to database.")
    dbAccess.telemetry_add(device, tele_valid_data)

    # Rules Engine
    print("Sending to rules engine.")
    rules_engine()

    return tele_valid_data, 200

# Placeholders
def anomaly_detect():
    
    return True


def rules_engine():

    return True



# notes:

        # # passed to anomaly detection:
            # # # use anomaly functions
            # # # pass piece of data form of dictionary, name, returns true or false


        # # passed to rules engine

        # # observer design pattern