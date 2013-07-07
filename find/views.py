import json
from django.http import HttpResponse
from django.shortcuts import render
from mobileMMS.utilities.common import getSessionToken
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI




def find(request):

    accessToken = getSessionToken()
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

    return render(request, 'locationresults.html', locResponse)