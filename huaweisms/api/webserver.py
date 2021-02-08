import logging

from huaweisms.api.common import ApiCtx, get_from_url


logger = logging.getLogger(__name__)


def get_session_token_info(ctx):
    # type: (ApiCtx) -> ...
    """
    Get session token information

    :param ctx: ApiCtx instance
    :return:
    """

    url = "{}/webserver/SesTokInfo".format(ctx.api_base_url)
    return get_from_url(url, ctx=ctx, timeout=30)
