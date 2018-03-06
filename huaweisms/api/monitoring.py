from huaweisms.api.common import get_from_url, ApiCtx
from .config import API_URL


def status(ctx: ApiCtx):
    url = "{}/monitoring/status".format(API_URL)
    return get_from_url(url, ctx)
