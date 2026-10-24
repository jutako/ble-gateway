
import requests

class SensorDataReporter:

    host = None  # URL or IP of the HTTP version of sensor_data_backend
    port = None  # port
    endpoint = None # endpoint
    gateway_name = None  # sensor name to use

    def __init__(self, host: str, port: str, gateway_name:str, endpoint: str = "sendData"):

        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.gateway_name = gateway_name
        self.post_uri = f"http://{self.host}:{self.port}/{self.endpoint}"

    def make_record(self, device_mac, data):
        """Creates a full record for writing.
        """

        record = {
            "sensor": self.gateway_name,
            "device": device_mac,
            "payload": {
                "data_format": data['data_format'],
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

    def write(self, record: dict):
        r = requests.post(self.post_uri, json=record)
        return r
