from datetime import datetime

from huaweisms.api.common import post_to_url, ApiCtx, get_from_url
from .config import API_URL


def get_sms(ctx: ApiCtx, box_type: int = 1, page: int = 1, qty: int = 1):
    xml_data = """
        <request>
            <PageIndex>{}</PageIndex>
            <ReadCount>{}</ReadCount>
            <BoxType>{}</BoxType>
            <SortType>0</SortType>
            <Ascending>0</Ascending>
            <UnreadPreferred>1</UnreadPreferred>
        </request>    
    """.format(page, qty, box_type)

    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/sms/sms-list".format(API_URL)
    r = post_to_url(url, xml_data, ctx, headers)

    if r['type'] == 'response':
        if r['response']['Count']!='0':
            if type(r['response']['Messages']['Message']) == dict:
                m = r['response']['Messages']['Message']
                r['response']['Messages']['Message'] = []
                r['response']['Messages']['Message'].append(m)

    return r


def send_sms(ctx: ApiCtx, dest, msg: str):

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    if type(dest) == str:
        phones_content = '<Phone>{}</Phone>'.format(dest)
    else:
        phones_content = ""
        for phone in dest:
            phones_content += '<Phone>{}</Phone>\n'.format(phone)
    xml_data = """
        <request>
            <Index>-1</Index>
            <Phones>
            {}
            </Phones>
            <Sca></Sca>
            <Content>{}</Content>
            <Length>{}</Length>
            <Reserved>1</Reserved>
            <Date>{}</Date>
        </request> 
    """.format(phones_content, msg, len(msg), now_str)

    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/sms/send-sms".format(API_URL)
    r = post_to_url(url, xml_data, ctx, headers)
    return r


def delete_sms(ctx: ApiCtx, index: int):

    xml_data = """
        <?xml version:"1.0" encoding="UTF-8"?>
        <request>
            <Index>{}</Index>
        </request>
    """.format(index)

    headers = {
        '__RequestVerificationToken': ctx.token,
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = "{}/sms/delete-sms".format(API_URL)
    r = post_to_url(url, xml_data, ctx, headers)
    return r

def sms_count(ctx: ApiCtx):
    url = "{}/sms/sms-count".format(API_URL)
    return get_from_url(url, ctx)
