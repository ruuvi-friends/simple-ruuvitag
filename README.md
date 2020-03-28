# Simple Ruuvitag 🔧

Simple Ruuvitag is a hard frok and ***HEAVY*** simplification of [ttu work](https://github.com/ttu) [ruuvitag-sensor](https://github.com/ttu/ruuvitag-sensor)

It uses bleson python lib, which leverages Python 3 native support for Bluetooth sockets. 
However, in order for python to have access to AF_SOCKET family, python needs to be compiled with lib-bluetooth or bluez.

# Usage

## Simplest usage
Simplest usage is using ruuvi_client internal state.
The client will keep the latest state of all sensors that have been polled.

```python
macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D']
ruuvi_client = RuuviTagClient()
ruuvi_client.listen(mac_addresses=macs)

last_datas = ruuvi_client.get_current_datas()
print(last_datas)
```

However this means that if a sensor doesn't get updated in a while, the state will contain
old data that might pollute your dataset. To clear the state use the flag `consume=True` 

```python
last_datas = ruuvi_client.get_current_datas(consume=True)
```

## Callback usage

You cal also use a callback to handle data as it is recieved by the library.
Just pass a `callback` parameter to the listen method
```python
def handle_callback(data):
    print("Data from %s: %s" % (data[0], data[1]))

macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D']
ruuvi_client = RuuviTagClient()
ruuvi_client.listen(callback=handle_callback, mac_addresses=macs)
```

## Continous use:
Although the bluetooth observer is running, data might stop coming through.
For this we have `ruuvi_client.rescan()` witch will restart the observer, and data
should start flowing again.
```
ruuvi_client.listen()
time.sleep(5)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)
ruuvi_client.rescan()
time.sleep(5)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)
time.sleep(5)
```

Right now there seems to be no way to ask the observer to continuously provide 
all the advertisements - https://github.com/TheCellule/python-bleson/blob/master/bleson/core/roles.py

## Compatibility notes
Right now this library should work with:
* Python Docker official images (after this PR https://github.com/docker-library/python/pull/445)
* Latest Ubuntu versions
* Projects like HASS.io (after this PR https://github.com/home-assistant/docker-base/pull/53)

## FAQ

#### AttributeError: module 'socket' has no attribute 'AF_BLUETOOTH'

1. Isntall bluez or lib-bluetooth depending on your platfomr
2. rebuild your python eg: `sudo apt-get install --reinstall python3`