import time
from simple_ruuvitag.ruuvi import RuuviTagClient

ruuvi_client = RuuviTagClient()
ruuvi_client.start()

time.sleep(30)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)