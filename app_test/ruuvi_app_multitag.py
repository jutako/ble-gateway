from ruuvitag_sensor.ruuvi import RuuviTagSensor

# List of macs of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
tag1 = 'E2:42:6F:37:12:D9'
tag2 = 'DE:41:38:3F:44:59'
tag3 = 'D7:9C:82:BC:A8:1E'


def handle_data(found_data):
    print('MAC ' + found_data[0])
    print(found_data[1])
    print('\n')

macs = [tag1, tag2, tag3]
RuuviTagSensor.get_datas(handle_data, macs)
