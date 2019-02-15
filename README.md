[![Build Status](https://travis-ci.org/dopstar/huawei-modem-python-api-client.svg?branch=master)](https://travis-ci.org/dopstar/huawei-modem-python-api-client) [![Python Version](https://img.shields.io/pypi/pyversions/huawei-modem-api-client.svg)](https://pypi.python.org/pypi/huawei-modem-api-client) [![PyPI Status](https://img.shields.io/pypi/v/huawei-modem-api-client.svg)](https://pypi.python.org/pypi/huawei-modem-api-client)

# Modem USB Huawei HTTP API client in Python

This is a python lib to interact with Modem USB Huawei HTTP API. I tested it with:

* E5180
* E8372
* B315

Please let me know if you tested it successfully with other modems as well.

## Currently Supported

* webserver
   * SesTokInfo: gets a session token to use
* user
   * login: creates a new session on the HTTP API
* sms
   * get_sms: get information from boxes: inbox, outbox
   * send_sms: sends an SMS through device's modem
   * delete_sms: deletes an sms from one of their boxes
   * sms_count: get the sms count on each box
* ussd
   * status: get status of ussd. This will tell you if there are ussd messages available to read
   * send: sends a ussd message
   * get: retrieves a ussd message
* wlan:
    * get_connected_hosts: gets a list of connected devices
    * block_host: blocks the device from network
    * unblock_host: unblock device on network
    * get_blocked_hosts: gets a list of blocked devices
    * is_host_blocked: checks if device is blocked
* dialup:
    * connect_mobile: enables mobile (ie LTE / 4G / 3G / etc) network
    * disconnect_mobile: disables mobile network
    * get_mobile_status: checks the mobile connection status
* device:
    * reboot: reboots the modem

### Prerequisites

Only [`requests`](https://github.com/requests/requests) library (and its dependencies) is required.

This is `requirements.txt` content:

```
certifi==2018.1.18
chardet==3.0.4
idna==2.6
requests==2.0.0
```

### Installing

```bash
pip install huawei-modem-api-client
```

### Example
```python
import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms

ctx = huaweisms.api.user.quick_login("myusername", "mypassword")
print(ctx)
# output: <ApiCtx online>

# sending sms
huaweisms.api.sms.send_sms(
    ctx,
    'phone-number',
    'this is the sms message'
)

# connected devices
device_list = huaweisms.api.wlan.get_connected_hosts(ctx)

```

## Built With

* [requests](https://github.com/requests/requests) - Python HTTP Requests for Humans™

## Contributing

Send me a PM if you want to contribute. 

## Authors

* **Pablo Santa Cruz** - *Initial work* - [pablo](https://github.com/pablo)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

