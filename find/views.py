import json
from django.http import HttpResponse
from django.shortcuts import render
from mobileMMS.utilities.common import getSessionToken
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from mobileMMS.utilities.common import getEncryptedValue




def find(request):

    accessToken = getSessionToken(request)
    print 'access token: ' + accessToken

    apiFindLocationsParams = { "BrandID": None,
        "BusinessName": "",
        "FeatureLevel": None,
        "PageNumber": 1,
        "PageSize": 5,
        "SortBy": [
            {
                "SortBy": "Name",
                "SortDirection": 0
            }
        ],
        "UsePaging": True,
        "access_token": accessToken
    }

    cs = CustomerAPI()
    locResponse = cs.request("POST","locations", apiFindLocationsParams)

    response = render(request, 'locationresults.html', locResponse)
    response.set_cookie("user_session", getEncryptedValue(accessToken))
    return response