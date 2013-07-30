import json
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from django.conf import settings

from Crypto.Cipher import AES
import base64



def getSessionToken(request):

    accessToken = ""
    if "user_session" in request.COOKIES:
        accessToken = getDecryptedValue(request.COOKIES["user_session"])
        print "cookie session"
    else:
        print "non cookie session"
        apiAccessParams= {'client_id' : settings.APIKEY,
                  'client_secret' : settings.APISECRET,
                  'grant_type' :"client_credentials"
                  }

        cs = CustomerAPI()
        response = cs.request("GET","access_token", apiAccessParams)
        print(json.dumps(response, sort_keys=True, indent=4))
        accessToken = response['access_token']

    return accessToken

def getEncryptedValue(target):
    PADDING = '{'
    BLOCK_SIZE = 32
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    #prepare crypto method
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    cipher = AES.new(settings.SESSIONSECRET)
    encryptedTarget = EncodeAES(cipher, target)
    print 'Encrypted string:', encryptedTarget
    return encryptedTarget

def getDecryptedValue(target):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(settings.SESSIONSECRET)
    decryptedTarget = DecodeAES(cipher, target)
    print 'Decrypted string:', decryptedTarget
    return decryptedTarget

def getSessionDictionary(request):
    session = {}
    if "user" in request.COOKIES:
        session['user'] = request.COOKIES['user']
    if "user_session" in request.COOKIES:
        session['user_session'] = request.COOKIES['user_session']
    if "name" in request.COOKIES:
        session['name'] = request.COOKIES['name']
    if "location" in request.COOKIES:
        session['location'] = request.COOKIES['location']

    return session