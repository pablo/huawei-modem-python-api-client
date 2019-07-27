from huaweisms.api.common import post_to_url, ApiCtx, get_from_url


def status(ctx):
    # type: (ApiCtx) -> ...
    url = "{}/ussd/status".format(ctx.api_base_url)
    return get_from_url(url, ctx)


def get(ctx):
    # type: (ApiCtx) -> ...
    url = "{}/ussd/get".format(ctx.api_base_url)
    return get_from_url(url, ctx)


def send(ctx, msg):
    # type: (ApiCtx, str) -> ...
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
    url = "{}/ussd/send".format(ctx.api_base_url)
    r = post_to_url(url, xml_data, ctx, headers)
    return r
