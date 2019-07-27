from huaweisms.api.common import get_from_url, ApiCtx


def status(ctx):
    # type: (ApiCtx) -> dict
    url = "{}/monitoring/status".format(ctx.api_base_url)
    return get_from_url(url, ctx)
