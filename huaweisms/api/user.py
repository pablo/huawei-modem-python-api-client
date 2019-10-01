import base64

import hashlib

import binascii

import json

import huaweisms.api.webserver
from huaweisms.api.common import common_headers, ApiCtx, post_to_url, get_from_url


def b64_sha256(data):
    # type: (str) -> str
    s256 = hashlib.sha256()
    s256.update(data.encode('utf-8'))
    dg = s256.digest()
    hs256 = binascii.hexlify(dg)
    return base64.urlsafe_b64encode(hs256).decode('utf-8', 'ignore')


def quick_login(username, password, modem_host=None):
    # type: (str, str, str) -> ...
    ctx = ApiCtx(modem_host=modem_host)
    token = huaweisms.api.webserver.get_session_token_info(ctx.api_base_url)
    session_token = token['response']['SesInfo'].split("=")
    ctx.session_id = session_token[1] if len(session_token) > 1 else session_token[0]
    ctx.login_token = token['response']['TokInfo']
    response = login(ctx, username, password)
    if not ctx.logged_in:
        raise ValueError(json.dumps(response))
    return ctx


def login(ctx, user_name, password):
    # type: (ApiCtx, str, str) -> ...
    headers = common_headers()
    url = "{}/user/login".format(ctx.api_base_url)

    password_value = b64_sha256(user_name + b64_sha256(password) + ctx.login_token)

    xml_data = """
    <?xml version:"1.0" encoding="UTF-8"?>
    <request>
        <Username>{}</Username>
        <Password>{}</Password>
        <password_type>4</password_type>
    </request>
    """.format(user_name, password_value)

#   setup headers
    headers['__RequestVerificationToken'] = ctx.login_token
    headers['X-Requested-With'] = 'XMLHttpRequest'

    r = post_to_url(url, xml_data, ctx, headers)

    if r['type'] == "response" and r['response'] == "OK":
        ctx.logged_in = True

    return r


def state_login(ctx):
    # type: (ApiCtx) -> ...
    url = "{}/user/state-login".format(ctx.api_base_url)
    return get_from_url(url, ctx)
