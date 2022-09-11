""" A class to handle writing of records to InfluxDB 2.x

Supports:
* ruuvitag

"""
import os
import json

from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS

from typing import List

class InfluxDB2Reporter:

    influx_client = None  # connection to InfluxDB
    database = None  # name of database
    gateway_name = None # name of gateway to operate in

    def __init__(
        self,
        influx_host:str,
        influx_port: str,
        organisation: str,
        token: str,
        bucket: str,
        gateway_name: str=None) -> None:
        
        # Create influx_client
        self.influx_client = InfluxDBClient(
            url=f"{influx_host}:{influx_port}",
            org=organisation,
            token=token,   
        )

        self.bucket = bucket

        # Set gateway name, helps identify logger devices
        if gateway_name is None:
            try:
                self.gateway_name = os.environ['BALENA_DEVICE_NAME_AT_INIT']
            except:
                self.gateway_name = 'generic-gateway'
        else:
            self.gateway_name = gateway_name


    #def connect_influx(self, host, port):
    #    return InfluxDBClient(host=host, port=port)

    def write_influx(points: List[Point]) -> None:

        write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)

        write_api.write(bucket=self.bucket, record=points)

    
    #def disconnect_influx(self):
    #    self.influx_client.close()

    def make_ruuvitag_record_raspigw(self, device_mac: str, data: dict) -> Point:
        """Creates a full record of type Point() for writing to InfluxDB 2.x.
        """

        point = (
            Point("ruuvitag")

            .tag("gateway", self.gateway_name)
            .tag("mac", device_mac)
            .tag("data_format", data['data_format'])

            .field("temperature", data["temperature"])
            .field("humidity", data["humidity"])
            .field("pressure", data["pressure"])
            .field("acc_x", data["acceleration_x"])
            .field("acc_y", data["acceleration_y"])
            .field("acc_z", data["acceleration_z"])
            .field("acc", data["acceleration"])
            .field("battery", data["battery"])
        )

        return point

    def make_ruuvitag_dict(self, device_mac, data):
        """Creates a full record for writing. From InfluxDB version 1.x
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
        """ For InfluxDB version 1.x
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
