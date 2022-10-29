[![Build Status](https://github.com/dopstar/huawei-modem-python-api-client/workflows/build/badge.svg?branch=master)](https://github.com/dopstar/huawei-modem-python-api-client/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/dopstar/huawei-modem-python-api-client/branch/master/graph/badge.svg)](https://codecov.io/gh/dopstar/huawei-modem-python-api-client)
[![Python Version](https://img.shields.io/pypi/pyversions/huawei-modem-api-client.svg)](https://pypi.python.org/pypi/huawei-modem-api-client)
[![PyPI Status](https://img.shields.io/pypi/v/huawei-modem-api-client.svg)](https://pypi.python.org/pypi/huawei-modem-api-client)
[![PyPI Downloads](https://img.shields.io/pypi/dm/huawei-modem-api-client.svg)](https://pypi.python.org/pypi/huawei-modem-api-client)
[![Licence](https://img.shields.io/github/license/pablo/huawei-modem-python-api-client.svg)](https://raw.githubusercontent.com/pablo/huawei-modem-python-api-client/master/LICENSE.md)

# Python HTTP API client for Huawei Modems

This is a python library to interact with a Huawei modem over HTTP API.

The library has been tested on these devices:
* E5180
* E8372
* B315
* B529s-23a
* H122-373 (HUAWEI 5G CPE Pro 2 locoked to the UK Network Three)

Please let me know if you tested it successfully with other modems as well.

## Currently Supported

* webserver
   * get_session_token_info: gets a session token to use
* user
   * login: creates a new session on the HTTP API
   * logout: deletes current session on the HTTP API
* sms
   * get_sms: get information from boxes: inbox, outbox
   * send_sms: sends an SMS through device's modem
   * delete_sms: deletes an sms from one of their boxes
   * sms_count: get the sms count on each box
   * sms_set_read: set the sms status to read
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
    * switch_wlan_24ghz: allows to switch on or off the wlan 2.4Ghz module of the router
    * switch_wlan_5ghz: allows to switch on or off the wlan 5Ghz module of the router
* dialup:
    * connect_mobile: enables mobile (ie LTE / 4G / 3G / etc) network
    * disconnect_mobile: disables mobile network
    * get_mobile_status: checks the mobile connection status
* device:
    * reboot: reboots the modem

### Prerequisites

[`requests`](https://github.com/requests/requests) library (and its dependencies) is required.
[`six`](https://pypi.org/project/six/) library (and its dependencies for Python 2 and 3 compatibility)
[`typing`](https://docs.python.org/3/library/typing.html) library (support for type hints)

This is `requirements.txt` content:

```
requests>=2.25.1
six>=1.15.0
typing>=3.7.4.3
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
# output: <ApiCtx modem_host=192.168.8.1>

# sending sms
huaweisms.api.sms.send_sms(
    ctx,
    'phone-number',
    'this is the sms message'
)

# connected devices
device_list = huaweisms.api.wlan.get_connected_hosts(ctx)

```

Note: The default modem host is assumed to be `192.168.8.1`. If that is not the case for you, you can specify your modem ip as follows:

```python
import huaweisms.api.user
ctx = huaweisms.api.user.quick_login("myusername", "mypassword", modem_host='10.11.12.13')
print(ctx)

#output: <ApiCtx modem_host=10.11.12.13>
```

### HTTPS Examples

When the router uses HTTPS instead of HTTP, you can pass the `uri_scheme` when creating the context instance which
becomes used on subsequent api calls that use the same context.
```python
import huaweisms.api.user
ctx = huaweisms.api.user.quick_login(
  'username',
  'password',
  modem_host='192.168.12.13',
  uri_scheme='https'
)
```

If the router that uses HTTPS uses self-signed certificates, there will be SSL errors. You can ignore certificate 
validation/verification as follows:
```python
import huaweisms.api.user
ctx = huaweisms.api.user.quick_login(
  'username',
  'password',
  modem_host='192.168.12.13',
  uri_scheme='https',
  verify=False
)
```

## Built With

* [requests](https://github.com/requests/requests) - Python HTTP Requests for Humans™

## Contributing

Send me a PM if you want to contribute. 

## Authors

* **Pablo Santa Cruz** - *Owner* - [pablo](https://github.com/pablo)
* **Mka Madlavana** - *Collaborator* - [dopstar](https://github.com/dopstar)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

