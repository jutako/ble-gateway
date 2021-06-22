from ruuvitag_sensor.ruuvi import RuuviTagSensor
from datetime import datetime
from influxdb2_reporter import InfluxDB2Reporter
from config_local import (
    SENSOR_MAC_ARR,
    MIN_REPORT_INTERVAL_SEC,
    INFLUX_HOST,
    INFLUX_PORT,
    INFLUX_ORGANISATION,
    INFLUX_TOKEN,
    INFLUX_BUCKET,
    VERBOSE
)

# Initialize

# Dict of sensors, MAC address as key
# last_reported_ts: datetime.datetime when values were reported last time, used for rate limiting
now_ts = datetime.now()
sensors = dict((el, {'last_reported_ts': now_ts}) for el in SENSOR_MAC_ARR)
#print(sensors)

# Reporter instance (influxdb connection, record creation, writing)
rp = InfluxDB2Reporter(INFLUX_HOST, INFLUX_PORT, INFLUX_ORGANISATION, INFLUX_TOKEN)
# print(rp.client)
#rp.disconnect_influx() # could be added to possible on_exit() routine

# Handler for received data
def handle_data(data):
    """
    :param data: two element list with device MAC as str and data as dict.
    """

    #print(data)
    #rp.write_influx(INFLUX_BUCKET, [rp.make_ruuvitag_point(data[0], data[1])])

    try:
        last_seen_ts = sensors[data[0]]['last_reported_ts']  # data[0] might not be in the dict?

        if (datetime.now() - last_seen_ts).total_seconds() > MIN_REPORT_INTERVAL_SEC:
            # Report values
            if VERBOSE:
                print('MAC ' + data[0])
                print(data[1])
                print('\n')

            rp.write_influx(INFLUX_BUCKET, [rp.make_ruuvitag_point(data[0], data[1])])

            sensors[data[0]]['last_reported_ts'] = datetime.now()

        else:
            # Do not report
            #if VERBOSE:
            #    print('Too litlle time passed.')
            pass
    except:
        print('Found tag ' + data[0] + ' which is not listed.')


# Start the handler
# Loops forever?
RuuviTagSensor.get_datas(handle_data, SENSOR_MAC_ARR)
