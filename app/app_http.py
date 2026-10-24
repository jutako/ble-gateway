"""Main ruuvi tag listener app

This version works with mqtt_sensor_data_backend http version.

"""
import os
from datetime import datetime
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from sensor_data_reporter import SensorDataReporter

HOST = os.environ["SENSOR_DATA_HOST"]
PORT = os.environ["SENSOR_DATA_PORT"]
GATEWAY_NAME = os.environ["GATEWAY_NAME"]

# Initialize
reporter = SensorDataReporter(host = HOST, port = PORT, gateway_name=GATEWAY_NAME)

# Handler for received data
def handle_data(data):
    """
    :param data: two element list with device MAC as str and data as dict.
    """

    print(data[0])
    print(data[1])

    record = reporter.make_record(data[0], data[1])
    r = reporter.write(record)
    print(r)


if __name__=="__main__":
    # Start the handler
    # Loops forever?
    RuuviTagSensor.get_data(handle_data)
