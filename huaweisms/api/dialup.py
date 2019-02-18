import huaweisms.api.common
from huaweisms.api.config import API_URL


XML_TEMPLATE = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<request>'
    '<dataswitch>{enable}</dataswitch>'
    '</request>'
)


def connect_mobile(ctx: huaweisms.api.common.ApiCtx):
    return switch_mobile_on(ctx)


def disconnect_mobile(ctx: huaweisms.api.common.ApiCtx):
    return switch_mobile_off(ctx)


def get_mobile_status(ctx: huaweisms.api.common.ApiCtx):
    url = "{}/dialup/mobile-dataswitch".format(API_URL)
    result = huaweisms.api.common.get_from_url(url, ctx)
    if result and result.get('type') == 'response':
        response = result['response']
        if response and response.get('dataswitch') == '1':
            return 'CONNECTED'
        if response and response.get('dataswitch') == '0':
            return 'DISCONNECTED'
    return 'UNKNOWN'


def switch_mobile_off(ctx: huaweisms.api.common.ApiCtx):
    data = XML_TEMPLATE.format(enable=0)
    headers = {
        '__RequestVerificationToken': ctx.token,
    }
    url = "{}/dialup/mobile-dataswitch".format(API_URL)
    return huaweisms.api.common.post_to_url(url, data, ctx, additional_headers=headers)


def switch_mobile_on(ctx: huaweisms.api.common.ApiCtx):
    data = XML_TEMPLATE.format(enable=1)
    headers = {
        '__RequestVerificationToken': ctx.token,
    }
    url = "{}/dialup/mobile-dataswitch".format(API_URL)
    return huaweisms.api.common.post_to_url(url, data, ctx, additional_headers=headers)
