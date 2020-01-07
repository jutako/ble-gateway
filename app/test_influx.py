
from influxdb import InfluxDBClient
import json
import time
from reporter import Reporter

influx_host = "157.230.98.123"
influx_port = 8087
influx_db = 'sensor_raspigw'

device_mac = 'AA:11:BB:22:CC:D3'
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


rp = Reporter(influx_host, influx_port, influx_db)

print(rp.make_ruuvitag_record_raspigw(device_mac, data))
print(rp.write_influx([rp.make_ruuvitag_record_raspigw(device_mac, data)]))
time.sleep(2)
rp.write_influx([rp.make_ruuvitag_record_raspigw(device_mac, data)])


rp.disconnect_influx()


"""
db_client = reporter.connect_influx(influx_host, influx_port)
reporter.write_influx(db_client, 'influx', data_dict)
"""

"""
influx_client = InfluxDBClient(host=influx_host, port=influx_port)
influx_client.switch_database(influx_db)
influx_client.write_points([data_dict])
influx_client.close()
"""
