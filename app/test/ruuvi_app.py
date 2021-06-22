from ruuvitag_sensor.ruuvi import RuuviTagSensor

# List of macs of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
tag1 = 'CA:35:EF:13:E5:EB'



def handle_data(found_data):
    print('MAC ' + found_data[0])
    print(found_data[1])



macs = [tag1]
RuuviTagSensor.get_datas(handle_data, macs)
