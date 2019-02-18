from huaweisms.api.common import (
    post_to_url,
    get_from_url,
    ApiCtx,
)
from .config import API_URL


def information(ctx: ApiCtx) -> dict:
    url = "{}/device/information".format(API_URL)
    return get_from_url(url, ctx)


def basic_information(ctx: ApiCtx) -> dict:
    url = "{}/device/information".format(API_URL)
    return get_from_url(url, ctx)


def reboot(ctx: ApiCtx) -> dict:
    """
    Reboots the modem.
    """

    url = '{}/device/control'.format(API_URL)
    headers = {
        '__RequestVerificationToken': ctx.token,
    }

    payload = '<?xml version: "1.0" encoding="UTF-8"?><request><Control>1</Control></request>'
    return post_to_url(url, payload, ctx, additional_headers=headers)
