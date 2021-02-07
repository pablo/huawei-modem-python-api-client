from huaweisms.api.common import ApiCtx, get_from_url


def status(ctx):
    # type: (ApiCtx) -> dict
    url = "{}/monitoring/status".format(ctx.api_base_url)
    return get_from_url(url, ctx)
