import sys

from huaweisms.api import user, sms
from huaweisms.api.common import ApiCtx


USER = "admin"
PASSWORD = ""
PHONE_NUMBER = ""


def get_session():
    return user.quick_login(USER, PASSWORD)


def valid_context(ctx):
    # type: (ApiCtx) -> ...
    sl = user.state_login(ctx)
    if sl['type'] == 'response' and sl['response']['State'] != -1:
        return True
    return False


if __name__ == '__main__':
    # USAGE: python3 sendmsg.py <password> <number> <message>
    # Arguments are <program> <password> <to_phone> <message>
    if len(sys.argv) != 4:
        print('Incomplete arguments ', len(sys.argv) - 1, 'received, 3 required')
        print('USAGE:', sys.argv[0], '"admin password" "phone number" "message"')
        exit()

    PASSWORD = sys.argv[1]
    PHONE_NUMBER = sys.argv[2]
    MESSAGE = sys.argv[3]

    ctx = get_session()
    sent = sms.send_sms(ctx, PHONE_NUMBER, MESSAGE)

    if sent['type'] == "response" and sent['response'] == "OK":
        print("Message sent.")
    else:
        print("Message error")
