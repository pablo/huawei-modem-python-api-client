from huaweisms.api.common import get_from_url, post_to_url


def get_net_mode(ctx):
    # type: (ApiCtx) -> dict
    url = "{}/net/net-mode".format(ctx.api_base_url)
    return get_from_url(url, ctx)


def get_net_mode_list(ctx):
    # type: (ApiCtx) -> dict
    url = "{}/net/net-mode-list".format(ctx.api_base_url)
    return get_from_url(url, ctx)


def set_net_mode(ctx, net_mode, net_band, lte_band):
    # type: (ApiCtx, str, str, str) -> ...
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <NetworkMode>{}</NetworkMode>
            <NetworkBand>{}</NetworkBand>
            <LTEBand>{}</LTEBand>
       </request>""".format(net_mode, net_band, lte_band)
    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/api/net/net-mode".format(ctx.api_base_url)
    r = post_to_url(url, xml_data, ctx, headers)
    return r


def register(ctx, mode, plmn = "", rat = ""):
    # type: (ApiCtx, str, str, str) -> ...
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
                  <request>
                    <Mode>{}</Mode>
                    <Plmn>{}</Plmn>
                    <Rat>{}</Rat>
                  </request>""".format(mode, plmn, rat)
    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/api/net/register".format(ctx.api_base_url)
    r = post_to_url(url, xml_data, ctx, headers)
    return r
