

import json
import requests

from pprint import pprint

HOST = "192.168.20.200"
PORT = 5001
ENDPOINT = 'sendData'

device_mac = 'AA:11:BB:22:CC:33'
data = {
    'data_format': 3,
    'battery': 2959, 
    'temperature': 19.56, 
    'pressure': 1018.55,
    'humidity': 25.5,
    'acceleration_x': -862,
    'acceleration_z': -645,
    'acceleration_y': -84,
    'acceleration': 1079.872677680105
}


post_payload = {
    "sensor": "ruuvitagtest",
    "device": device_mac,
    "payload": data
}
pprint(post_payload)


#print(json.dumps(post_payload))

#r = requests.post(f"http://{HOST}:{PORT}/{ENDPOINT}", json=post_payload)
#print(r)


from sensor_data_reporter import SensorDataReporter

reporter = SensorDataReporter(host = HOST, port = PORT, gateway_name="ruuvitag_reporter_test")

record = reporter.make_record(device_mac, data)
r = reporter.write(record)
print(r)