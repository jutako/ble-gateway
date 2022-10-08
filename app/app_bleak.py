"""Main ruuvi tag listener app using OS independent async Bleak

# TODO
* reporter.disconnect_influx() # could be added to possible on_exit() routine
"""

from datetime import datetime
import os
os.environ['RUUVI_BLE_ADAPTER'] = 'bleak'

import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor

from config import (
    MIN_REPORT_INTERVAL_SEC,
    INFLUX_VERSION,
    INFLUX_HOST,
    INFLUX_PORT,
    VERBOSE
)

# Reporter instance (influxdb connection, record creation, writing)
if INFLUX_VERSION == 1:
    from config import INFLUX_DB
    from reporter import Reporter
    reporter = Reporter(INFLUX_HOST, INFLUX_PORT, INFLUX_DB)
    # Note: no authentication!

elif INFLUX_VERSION == 2:
    from config import (
        INFLUX_ORGANISATION,
        INFLUX_TOKEN,
        INFLUX_BUCKET,
    )
    from influxdb2_reporter import InfluxDB2Reporter
    reporter = InfluxDB2Reporter(INFLUX_HOST, INFLUX_PORT, INFLUX_ORGANISATION, INFLUX_TOKEN, INFLUX_BUCKET)

else:
    raise ValueError(f"Constant INFLUX_VERSION can be 1 or 2, not '{INFLUX_VERSION}'.")

# Initialize

# Dict of sensor states, MAC address as key.
# sensor_states = {
#     "AA:BB:CC": {
#         "last_reported_ts": datetime.datetime
#     },
#     ...
# }
# last_reported_ts: datetime.datetime when values were reported last time, used for rate limiting.
sensor_states = dict()  # keys are added as devices are encountered

if VERBOSE:
    print(reporter.influx_client)
    print(sensor_states)


# Handler for received data
def handle_data(data: list) -> None:
    """Data handling

    :param data: Two element list with device MAC as str and data as dict.
    :return: Save data to InfluxDB and/or HTTP REST API
    """

    device_mac = data[0]
    device_data = data[1]

    if device_mac not in sensor_states.keys():
        sensor_states[device_mac] = {'last_reported_ts': datetime.now()}

    
    if VERBOSE:
        print(data)
        print([reporter.make_ruuvitag_record_raspigw(device_mac, device_data)])

    
    last_seen_ts = sensor_states[device_mac]['last_reported_ts']

    if (datetime.now() - last_seen_ts).total_seconds() > MIN_REPORT_INTERVAL_SEC:
            
        try:
            # TODO: Make reporting functions catch their own errors

            # InfluxDB
            reporter.write_influx(
                [reporter.make_ruuvitag_record_raspigw(device_mac, device_data)]
            )

            # MQTT (e.g. Balena blocks style)
            # TODO

            # HTTP REST API
            # TODO

        except Exception as e:
            print(e)

        # Update last reported ts
        sensor_states[device_mac]['last_reported_ts'] = datetime.now()

        if VERBOSE:
            print(f"MAC: {device_mac}")
            print("Data:")
            print(device_data)


async def main():
    """Main operation loop
    """
    async for data in RuuviTagSensor.get_data_async():
        handle_data(data)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
