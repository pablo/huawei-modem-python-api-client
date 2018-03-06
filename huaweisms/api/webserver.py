from huaweisms.api.common import get_from_url
from .config import API_URL


def SesTokInfo():
    url = "{}/webserver/SesTokInfo".format(API_URL)
    return get_from_url(url)
