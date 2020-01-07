from ruuvitag_sensor.ruuvi import RuuviTagSensor
from datetime import datetime
from reporter import Reporter

# Setup

# List of MAC addresses of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
SENSOR_MAC_ARR = [
    'E2:42:6F:37:12:D9',
    'DE:41:38:3F:44:59',
    'D7:9C:82:BC:A8:1E'
]

MIN_REPORT_INTERVAL_SEC = 30
INFLUX_HOST = "157.230.98.123"
INFLUX_PORT = 8087
INFLUX_DB = 'sensor_raspigw'
VERBOSE = True

# Initialize

# Dict of sensors, MAC address as key
# last_reported_ts: datetime.datetime when values were reported last time, used for rate limiting
now_ts = datetime.now()
sensors = dict((el, {'last_reported_ts': now_ts}) for el in SENSOR_MAC_ARR)
#print(sensors)

# Reporter instance (influxdb connection, record creation, writing)
rp = Reporter(INFLUX_HOST, INFLUX_PORT, INFLUX_DB)
#rp.disconnect_influx() # could be added to possible on_exit() routine

# Handler for received data
def handle_data(data):
    """
    :param data: two element list with device MAC as str and data as dict.
    """

    try:
        last_seen_ts = sensors[data[0]]['last_reported_ts']  # data[0] might not be in the dict?

        if (datetime.now() - last_seen_ts).total_seconds() > MIN_REPORT_INTERVAL_SEC:
            # Report values
            if VERBOSE:
                print('MAC ' + data[0])
                print(data[1])
                print('\n')

            rp.write_influx([rp.make_ruuvitag_record_raspigw(data[0], data[1])])

            sensors[data[0]]['last_reported_ts'] = datetime.now()

        else:
            # Do not report
            #if VERBOSE:
            #    print('Too litlle time passed.')
            pass
    except:
        print('Found tag ' + data[0] + 'which is not listed.')


# Start the handler
# Loops forever?
RuuviTagSensor.get_datas(handle_data, SENSOR_MAC_ARR)
