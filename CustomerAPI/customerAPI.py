#WSWrapper.py
import json
import urllib
import requests #HTTP library for Python, http://docs.python-requests.org/en/latest/
from django.conf import settings

#python version 3.2
class CustomerAPI:
    """Wrapper for API"""

    def request(self, requestType, method, params,**kwargs):
       

        if requestType.upper() == 'GET':
            url = settings.APIPATH + method + "?" +  urllib.urlencode(params)
            response = requests.get(url)

        if requestType.upper() == "POST":
            url = settings.APIPATH + method
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(params), headers=headers)

        if requestType.upper() == "PUT":
            url = settings.APIPATH + method
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, data=json.dumps(params), headers=headers)

        return response.json()
