from ruuvitag_sensor.ruuvi import RuuviTagSensor

# List of macs of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
tag1 = 'C3:60:95:50:C6:0E'



def handle_data(found_data):
    print('MAC ' + found_data[0])
    print(found_data[1])

macs = [tag1]
RuuviTagSensor.get_datas(handle_data, macs)
