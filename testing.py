import json
import requests #HTTP library for Python, http://docs.python-requests.org/en/latest/


apiFindLocationsParams = { "BrandID": None,
        "BusinessName": "",
        "FeatureLevel": None,
        "PageNumber": 1,
        "PageSize": 5,
        "UsePaging": 1,
        "access_token": "c88b1d56-a34b-4344-a924-3bdde5e2b115"
    }

url = "http://stable-app.secure-booker.com/WebService4/json/CustomerService.svc/locations"
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(apiFindLocationsParams), headers=headers)
print (response)