import json
from django.http import HttpResponse
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from django.conf import settings


def getSessionToken():
    apiAccessParams= {'client_id' : settings.APIKEY,
                  'client_secret' : settings.APISECRET,
                  'grant_type' :"client_credentials"
                  }

    cs = CustomerAPI()
    response = cs.request("GET","access_token", apiAccessParams)
    print(json.dumps(response, sort_keys=True, indent=4))

    return response['access_token']
