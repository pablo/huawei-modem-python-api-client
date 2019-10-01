import logging
from typing import Union
from xml.dom.minidom import Element

import requests
from huaweisms.api.config import MODEM_HOST

from huaweisms.xml.util import get_child_text, parse_xml_string, get_dictionary_from_children


logger = logging.getLogger(__name__)


class ApiCtx:

    def __init__(self, modem_host=None):
        # type: (...) -> None
        self.session_id = None
        self.logged_in = False
        self.login_token = None
        self.tokens = []
        self.__modem_host = modem_host if modem_host else MODEM_HOST

    def __unicode__(self):
        return '<{} modem_host={}>'.format(
            self.__class__.__name__,
            self.__modem_host
        )

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    @property
    def api_base_url(self):
        return 'http://{}/api'.format(self.__modem_host)

    @property
    def token(self):
        if not self.tokens:
            logger.warning('You ran out of tokens. You need to login again')
            return None
        return self.tokens.pop()


def common_headers():
    return {
        "X-Requested-With": "XMLHttpRequest"
    }


def check_error(elem):
    # type: (Element) -> Union[dict, None]
    if elem.nodeName != "error":
        return None

    return {
        "type": "error",
        "error": {
            "code": get_child_text(elem, "code"),
            "message": get_child_text(elem, "message")
        }
    }


def api_response(r):
    # type: (requests.Response) -> dict
    if r.status_code != 200:
        r.raise_for_status()

    xmldoc = parse_xml_string(r.text)

    err = check_error(xmldoc.documentElement)
    if err:
        return err

    return {
        "type": "response",
        "response": get_dictionary_from_children(xmldoc.documentElement)
    }


def check_response_headers(resp, ctx):
    # type: (..., ApiCtx) -> ...
    if '__RequestVerificationToken' in resp.headers:
        toks = [x for x in resp.headers['__RequestVerificationToken'].split("#") if x != '']
        if len(toks) > 1:
            ctx.tokens = toks[2:]
        elif len(toks) == 1:
            ctx.tokens.append(toks[0])

    if 'SessionID' in resp.cookies:
        ctx.session_id = resp.cookies['SessionID']


def post_to_url(url, data, ctx=None, additional_headers=None):
    # type: (str, str, ApiCtx, dict) -> dict
    cookies = build_cookies(ctx)
    headers = common_headers()

    if additional_headers:
        headers.update(additional_headers)

    r = requests.post(url, data=data, headers=headers, cookies=cookies)
    check_response_headers(r, ctx)
    return api_response(r)


def get_from_url(url, ctx=None, additional_headers=None, timeout=None):
    # type: (str, ApiCtx, dict, int) -> dict
    cookies = build_cookies(ctx)
    headers = common_headers()

    if additional_headers:
        headers.update(additional_headers)

    r = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
    check_response_headers(r, ctx)
    return api_response(r)


def build_cookies(ctx):
    # type: (ApiCtx) -> ...
    cookies = None
    if ctx and ctx.session_id:
        cookies = {
            'SessionID': ctx.session_id
        }
    return cookies
