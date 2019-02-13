from huaweisms.api.common import get_from_url, ApiCtx
from .config import API_URL


def get_connected_hosts(ctx: ApiCtx):
    url = "{}/wlan/host-list".format(API_URL)
    return get_from_url(url, ctx)
