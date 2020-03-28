import time
from simple_ruuvitag.ruuvi import RuuviTagClient

macs = ['CD:81:78:21:E0:81']
ruuvi_client = RuuviTagClient()
# ruuvi_client.listen(mac_addresses=macs)
ruuvi_client.listen()


time.sleep(5)
last_datas = ruuvi_client.get_current_datas()

print(last_datas)
    
ruuvi_client.rescan()
time.sleep(5)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)
    
time.sleep(5)
