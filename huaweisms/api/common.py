from xml.dom.minidom import Element

import requests

from huaweisms.xml.util import get_child_text, parse_xml_string, get_dictionary_from_children


class ApiCtx(object):

    def __init__(self) -> None:
        self.session_id = None
        self.logged_in = False
        self.token = None
        self.tokens = []

    def __unicode__(self):
        return '<{} {}>'.format(
            self.__class__.__name__,
            'online' if self.logged_in else 'offline'
        )

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


def common_headers():
    return {
        "X-Requested-With": "XMLHttpRequest"
    }


def check_error(elem: Element) -> dict:
    if elem.nodeName != "error":
        return None

    return {
        "type": "error",
        "error": {
            "code": get_child_text(elem, "code"),
            "message": get_child_text(elem, "message")
        }
    }


def api_response(r: requests.Response) -> dict:
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


def check_response_headers(resp, ctx: ApiCtx):
    if '__RequestVerificationToken' in resp.headers:
        toks = [x for x in resp.headers['__RequestVerificationToken'].split("#") if x != '']
        if len(toks) > 1:
            ctx.tokens = toks[2:]
        elif len(toks) == 1:
            ctx.tokens.append(toks[0])

    if 'SessionID' in resp.cookies:
        ctx.session_id = resp.cookies['SessionID']


def post_to_url(url: str, data: str, ctx: ApiCtx = None, additional_headers: dict = None) -> dict:
    headers = common_headers()

    if additional_headers:
        headers.update(additional_headers)

    cookies = None
    if ctx and ctx.session_id:
        cookies = {
            'SessionID': ctx.session_id
        }

    r = requests.post(url, data=data, headers=headers, cookies=cookies)

    check_response_headers(r, ctx)

    return api_response(r)


def get_from_url(url: str, ctx: ApiCtx = None, additional_headers: dict = None) -> dict:

    headers = common_headers()

    if additional_headers:
        headers.update(additional_headers)

    cookies = None
    if ctx and ctx.session_id:
        cookies = {
            'SessionID': ctx.session_id
        }
    r = requests.get(url, headers=headers, cookies=cookies)

    check_response_headers(r, ctx)

    return api_response(r)

