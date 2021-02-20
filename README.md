[![Build Status](https://travis-ci.org/ruuvi-friends/simple-ruuvitag.svg?branch=master)](https://travis-ci.org/ruuvi-friends/simple-ruuvitag)

# Simple Ruuvitag 🔧

Simple Ruuvitag is a hard frok and ***HEAVY*** simplification of [ttu work](https://github.com/ttu) [ruuvitag-sensor](https://github.com/ttu/ruuvitag-sensor)

It uses bleson python lib, which leverages Python 3 native support for Bluetooth sockets. 
However, in order for python to have access to AF_SOCKET family, python needs to be compiled with lib-bluetooth or bluez.

**⚠️ This is a recent library with no guarantee of stability. There might be breaking changes so use the release tags to pull specific version**

# Installation
```
pip install simple-ruuvitag
```

# Usage

## Simplest usage
Simplest usage is using ruuvi_client internal state.
The client will keep the latest state of all sensors that have been polled.

```python
from simple_ruuvitag import RuuviTagClient
macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D']
ruuvi_client = RuuviTagClient(mac_addresses=macs)
ruuvi_client.start()

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
from simple_ruuvitag import RuuviTagClient
def handle_callback(mac_address, data):
	print(f"Data from {mac_address}: {data}")

macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D']
ruuvi_client = RuuviTagClient(callback=handle_callback, mac_addresses=macs)
ruuvi_client.start()
```

## Continous use:
Although the bluetooth observer is running, data might stop coming through due to
duplication removal in bleson. This issue is fixed in https://github.com/TheCellule/python-bleson/issues/40
and in simple-ruuvitag `v0.0.6`

If you still find this issue, simple-ruuvitag has a method for to re-scan:`ruuvi_client.rescan()` 
which will restart the observer, and data should start flowing again.
```
ruuvi_client.start()
time.sleep(5)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)
ruuvi_client.rescan()
time.sleep(5)
last_datas = ruuvi_client.get_current_datas()
print(last_datas)
time.sleep(5)
```

## Compatibility notes
Right now this library should work with:
* Python Docker official images (after this PR https://github.com/docker-library/python/pull/445)
* Latest Ubuntu versions
* Projects like HASS.io (after this PR https://github.com/home-assistant/docker-base/pull/53)
* MAC OS from version 0.0.3 
    * Unfortunately only for Ruuvi data format 5. Update your tags and use mode RAW V2
    * See how to update and change modes here - https://lab.ruuvi.com/ruuvitag-fw/

## FAQ

#### AttributeError: module 'socket' has no attribute 'AF_BLUETOOTH'

1. Install bluez or lib-bluetooth depending on your platform
2. Rebuild python.
