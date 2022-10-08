"""Main ruuvi tag listener app

#reporter.disconnect_influx() # could be added to possible on_exit() routine

"""
from datetime import datetime

from ruuvitag_sensor.ruuvi import RuuviTagSensor

from config import (
    SENSOR_MAC_ARR,
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

# Dict of sensor states, MAC address as key
# last_reported_ts: datetime.datetime when values were reported last time, used for rate limiting
now_ts = datetime.now()
sensor_states = dict((el, {'last_reported_ts': now_ts}) for el in SENSOR_MAC_ARR)

if VERBOSE:
    print(reporter.influx_client)
    print(sensor_states)


# Handler for received data
def handle_data(data):
    """
    :param data: two element list with device MAC as str and data as dict.
    """
    
    if VERBOSE:
        print(data)
        print([reporter.make_ruuvitag_record_raspigw(data[0], data[1])])

    try:
        last_seen_ts = sensor_states[data[0]]['last_reported_ts']  # data[0] might not be in the dict?

        if (datetime.now() - last_seen_ts).total_seconds() > MIN_REPORT_INTERVAL_SEC:
            # Report values

            reporter.write_influx(
                [reporter.make_ruuvitag_record_raspigw(data[0], data[1])]
            )

            sensor_states[data[0]]['last_reported_ts'] = datetime.now()

            print('MAC ' + data[0])
            print(data[1])
            
        else:
            # do not report
            pass

    except Exception as e:
        print(e)
        print('Found tag ' + data[0] + ' which is not listed.')


if __name__=="__main__":
    # Start the handler
    # Loops forever?
    RuuviTagSensor.get_data(handle_data, SENSOR_MAC_ARR)
