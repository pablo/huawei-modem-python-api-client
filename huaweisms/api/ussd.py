from huaweisms.api.common import post_to_url, ApiCtx, get_from_url
from .config import API_URL


def status(ctx: ApiCtx):
    url = "{}/ussd/status".format(API_URL)
    return get_from_url(url, ctx)


def get(ctx: ApiCtx):
    url = "{}/ussd/get".format(API_URL)
    return get_from_url(url, ctx)


def send(ctx: ApiCtx, msg: str):
    xml_data = """
        <?xml version="1.0" encoding="UTF-8"?>
        <request>
           <content>{}</content>
           <codeType>CodeType</codeType>
           <timeout></timeout>
        </request>
    """.format(msg)

    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/ussd/send".format(API_URL)
    r = post_to_url(url, xml_data, ctx, headers)
    return r

