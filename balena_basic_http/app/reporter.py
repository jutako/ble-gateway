
import os
import json
from influxdb import InfluxDBClient


class Reporter:

    influx_client = None  # connection to InfluxDB
    database = None  # name of database
    gateway_name = None # name of gateway to operate in

    def __init__(self, influx_host, influx_port, database_name, gateway_name=None):
        self.influx_client = self.connect_influx(influx_host, influx_port)
        self.database = database_name

        # Set gateway name, helps identify logger devices
        if gateway_name is None:
            try:
                self.gateway_name = os.environ['BALENA_DEVICE_NAME_AT_INIT']
            except:
                self.gateway_name = 'generic-gateway'
        else:
            self.gateway_name = gateway_name


    def connect_influx(self, host, port):
        return InfluxDBClient(host=host, port=port)

    def write_influx(self, list_of_data_dict):
        self.influx_client.switch_database(self.database)
        return self.influx_client.write_points(list_of_data_dict)
    
    def disconnect_influx(self):
        self.influx_client.close()

    def make_ruuvitag_record_raspigw(self, device_mac, data):
        """Creates a full record for writing.
        """

        record = {
            "measurement": "ruuvi",
            "tags": {
                "gateway": self.gateway_name,
                "mac": device_mac,
                "data_format": data['data_format']
            },
            "fields": {
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "pressure": data["pressure"],
                "acc_x": data["acceleration_x"],
                "acc_y": data["acceleration_y"],
                "acc_z": data["acceleration_z"],
                "acc": data["acceleration"],
                "battery": data["battery"]
            }
        }

        return record

    def to_influxjson(self, measurement, tags, fields):
        """
        influx_json = {
            "measurement": "alarms",
            "tags": {
                "deviceid": alarm_mqtt_json['id'],
                "type": alarm_mqtt_json['type'],
                "message": alarm_mqtt_json['message']
            },
            "fields": {
                "ntrigger": float(alarm_mqtt_json["ntrigger"])
            }
        }
        """

        influx_dict = {
            'measurement': measurement,
            'tags': tags,
            'fields': fields
        }

        return json.dumps(influx_dict)
