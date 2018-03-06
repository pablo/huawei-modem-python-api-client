from huaweisms.api.common import get_from_url, ApiCtx
from .config import API_URL


def information(ctx: ApiCtx) -> dict:
    url = "{}/device/information".format(API_URL)
    return get_from_url(url, ctx)


def basic_information(ctx: ApiCtx) -> dict:
    url = "{}/device/information".format(API_URL)
    return get_from_url(url, ctx)
