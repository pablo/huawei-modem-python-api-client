import logging

from huaweisms.api.common import get_from_url
from .config import API_URL


logger = logging.getLogger(__name__)


def SesTokInfo():
    logger.warning(
        '"%s.SesTokInfo()" is deprecated, use "%s.get_session_token_info()"',
        __name__,
        __name__
    )
    return get_session_token_info()


def get_session_token_info():
    url = "{}/webserver/SesTokInfo".format(API_URL)
    return get_from_url(url)
