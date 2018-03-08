import base64

import hashlib

import binascii

from huaweisms.api.common import common_headers, ApiCtx, post_to_url, get_from_url
from .config import API_URL


def b64_sha256(data: str) -> str:
    s256 = hashlib.sha256()
    s256.update(data.encode('utf-8'))
    dg = s256.digest()
    hs256 = binascii.hexlify(dg)
    return base64.urlsafe_b64encode(hs256).decode('utf-8', 'ignore')


def login(ctx: ApiCtx, user_name: str, password: str):
    headers = common_headers()
    url = "{}/user/login".format(API_URL)

#   original JS code:
#   psd = base64encode(
#    SHA256(
#        name +
#        base64encode(
#                       SHA256($('#password').val())
#        ) +
#        g_requestVerificationToken[0]
#    )
#   );

    password_value = b64_sha256(user_name + b64_sha256(password) + ctx.token)

    xml_data = """
    <?xml version:"1.0" encoding="UTF-8"?>
    <request>
        <Username>{}</Username>
        <Password>{}</Password>
        <password_type>4</password_type>
    </request>
    """.format(user_name, password_value)

#   setup headers
    headers['__RequestVerificationToken'] = ctx.token
    headers['X-Requested-With'] = 'XMLHttpRequest'

    r = post_to_url(url, xml_data, ctx, headers)

    if r['type'] == "response" and r['response'] == "OK":
        ctx.logged_in = True

    return r

def state_login(ctx: ApiCtx):
    url = "{}/user/state-login".format(API_URL)
    return get_from_url(url, ctx)

