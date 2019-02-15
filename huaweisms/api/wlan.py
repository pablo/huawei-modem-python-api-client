from huaweisms.api.config import API_URL
import huaweisms.api.common
import huaweisms.xml.util


def get_connected_hosts(ctx: huaweisms.api.common.ApiCtx):
    url = "{}/wlan/host-list".format(API_URL)
    return huaweisms.api.common.get_from_url(url, ctx)


def block_host(ctx: huaweisms.api.common.ApiCtx, mac_address: str, hostname: str = None):
    """
    Blocks/blacklists the given hosts.

    see http://192.168.8.1/html/wlanmacfilter.html
    """
    url = '{}/wlan/multi-macfilter-settings'.format(API_URL)
    if is_host_blocked(ctx, mac_address):
        return True

    response = get_blocked_hosts(ctx)['response']

    for ssid in response['Ssids']['Ssid']:
        for index in range(10):
            host_key = 'wifihostname{}'.format(index)
            mac_key = 'WifiMacFilterMac{}'.format(index)
            if ssid.get(host_key) == '' and ssid.get(mac_key) == '':
                ssid[host_key] = hostname or ''
                ssid[mac_key] = mac_address
                break
        else:
            raise ValueError('Failed to blacklist [{}], slots are full.'.format(mac_address))

    payload = huaweisms.xml.util.dict_to_xml({'request': response})
    headers = {
        '__RequestVerificationToken': ctx.token,
    }
    return huaweisms.api.common.post_to_url(url, payload, ctx, additional_headers=headers)


def unblock_host(ctx: huaweisms.api.common.ApiCtx, mac_address: str):
    """
    Unblocks/un-blacklists the given hosts.

    see http://192.168.8.1/html/wlanmacfilter.html
    """
    url = '{}/wlan/multi-macfilter-settings'.format(API_URL)
    if not is_host_blocked(ctx, mac_address):
        return True

    response = get_blocked_hosts(ctx)['response']

    for ssid in response['Ssids']['Ssid']:
        for index in range(10):
            host_key = 'wifihostname{}'.format(index)
            mac_key = 'WifiMacFilterMac{}'.format(index)
            if ssid.get(mac_key).lower() == mac_address.lower():
                ssid[host_key] = ''
                ssid[mac_key] = ''

    payload = huaweisms.xml.util.dict_to_xml({'request': response})
    headers = {
        '__RequestVerificationToken': ctx.token,
    }
    return huaweisms.api.common.post_to_url(url, payload, ctx, additional_headers=headers)


def get_blocked_hosts(ctx: huaweisms.api.common.ApiCtx):
    url = '{}/wlan/multi-macfilter-settings'.format(API_URL)
    return huaweisms.api.common.get_from_url(url, ctx)


def is_host_blocked(ctx: huaweisms.api.common.ApiCtx, mac_address: str) -> bool:
    response = get_blocked_hosts(ctx)
    if not response or response.get('type') != 'response':
        raise ValueError(response)

    ssids = response['response']['Ssids']['Ssid']
    for ssid in ssids:
        for k, v in ssid.items():
            if k.startswith('WifiMacFilterMac') and v.strip().lower() == mac_address.lower():
                return True
    return False
