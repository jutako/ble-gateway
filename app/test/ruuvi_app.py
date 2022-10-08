from ruuvitag_sensor.ruuvi import RuuviTagSensor

import ruuvitag_sensor.log

ruuvitag_sensor.log.enable_console()

# List of macs of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
tag1 = 'DD:E1:7C:BF:36:F4'



def handle_data(found_data):
    print('MAC ' + found_data[0])
    print(found_data[1])



macs = [tag1]
#macs = []
RuuviTagSensor.get_data(handle_data, macs)
