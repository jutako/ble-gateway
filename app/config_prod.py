# List of MAC addresses of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
# SENSOR_MAC_ARR = [
#     'E2:42:6F:37:12:D9',
#     'DE:41:38:3F:44:59',
#     'D7:9C:82:BC:A8:1E',
#     'D8:9F:A1:92:03:43',
#     'CA:35:EF:13:E5:EB',
#     'E3:F1:CA:6A:86:FA',
#     'F7:88:68:03:3F:FA',
#     'FA:43:18:72:4F:08',
#     'CF:6E:06:5E:67:93',
#     'EC:ED:E2:EB:EE:A0',
#     'CB:26:0A:17:A0:07',
#     'DD:E1:7C:BF:36:F4',
# ]

MIN_REPORT_INTERVAL_SEC = 30

INFLUX_HOST = "192.168.20.200"
INFLUX_PORT = 8086

INFLUX_VERSION = 1
INFLUX_DB = "ruuvi"

VERBOSE = False