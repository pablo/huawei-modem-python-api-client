from datetime import datetime

from huaweisms.api.common import post_to_url, ApiCtx, get_from_url


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
    url = "{}/sms/sms-list".format(ctx.api_base_url)
    r = post_to_url(url, xml_data, ctx, headers)

    if r['type'] == 'response':
        if r['response']['Count'] != '0':
            if isinstance(r['response']['Messages']['Message'], dict):
                m = r['response']['Messages']['Message']
                r['response']['Messages']['Message'] = [m]
    return r


def send_sms(ctx: ApiCtx, dest, msg: str):

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    dest = [dest] if isinstance(dest, str) else dest

    phones_content = '\n'.join('<Phone>{}</Phone>'.format(phone) for phone in dest)
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
    url = "{}/sms/send-sms".format(ctx.api_base_url)
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
    url = "{}/sms/delete-sms".format(ctx.api_base_url)
    r = post_to_url(url, xml_data, ctx, headers)
    return r


def sms_count(ctx: ApiCtx):
    url = "{}/sms/sms-count".format(ctx.api_base_url)
    return get_from_url(url, ctx)
