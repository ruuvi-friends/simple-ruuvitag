import time
from simple_ruuvitag.ruuvi import RuuviTagClient

macs = ['CD:81:78:21:E0:81']
ruuvi_client = RuuviTagClient()
ruuvi_client.listen(mac_addresses=macs)

last_datas = ruuvi_client.get_current_datas()

for i in range(10):
    
    print(last_datas)
    time.sleep(1)
    
ruuvi_client.stop()