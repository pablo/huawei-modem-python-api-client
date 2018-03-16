import sys
from pprint import pprint

from huaweisms.api import webserver, device, monitoring, user, sms, ussd
from huaweisms.api.common import ApiCtx

USER="admin"
PASSWORD=""
PHONE_NUMBER=""

# BEFORE running, do MAKE SURE heaweisms.api.config has the CORRECT VALUES for your MODEM

def get_session():
    ctx = ApiCtx()
    token = webserver.SesTokInfo()
    ctx.session_id = token['response']['SesInfo'].split("=")[1]
    ctx.token = token['response']['TokInfo']
    lgn = user.login(ctx, USER, PASSWORD)
    #pprint(lgn)
    return ctx


def valid_context(ctx: ApiCtx):
    sl = user.state_login(ctx)
    if sl['type'] == 'response' and sl['response']['State'] != -1:
        return True
    return False


# USAGE: python3 sendmsg.py <password> <number> <message>
# Arguments are <program> <password> <to_phone> <message>
if len(sys.argv) != 4:
   print('Incomplete arguments ', len(sys.argv)-1 , 'received, 3 required')
   print('USAGE:', sys.argv[0], '"admin password" "phone number" "message"')
   exit()

PASSWORD = sys.argv[1]
PHONE_NUMBER = sys.argv[2]
MESSAGE = sys.argv[3]

ctx = get_session()
sent = sms.send_sms(ctx, PHONE_NUMBER, MESSAGE)

#pprint(sent)

if sent['type']=="response" and sent['response']=="OK":
   print("Message sent.")
else:
   print("Message error")   
