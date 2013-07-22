import json
from django.http import HttpResponse
from django.shortcuts import redirect
from mobileMMS.login.forms import LoginForm
from django.shortcuts import render
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from mobileMMS.utilities.common import getEncryptedValue
from mobileMMS.utilities.common import getDecryptedValue
from django.conf import settings


def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            apiLoginParams = {
                "Email": cd["Email"],
                "LocationID": settings.APILOCATION,
                "Password": cd["Password"],
                "BrandID": None,
                "client_id": settings.APIKEY,
                "client_secret": settings.APISECRET,
                "grant_type": ""
            }

            cs = CustomerAPI()
            loginResponse = cs.request("POST","customer/login", apiLoginParams)

            response = render(request, 'loginresults.html', loginResponse)
            response.set_cookie("user_session", getEncryptedValue(loginResponse["access_token"]))
            response.set_cookie("user", loginResponse["Customer"]["CustomerID"])
            return response
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout(request):
    if "user_session" in request.COOKIES:
        print 'Cookie value: ', request.COOKIES["user_session"]
        apiLogoutParams = {
            "access_token": getDecryptedValue(request.COOKIES["user_session"])
        }
        cs = CustomerAPI()
        logoutResponse = cs.request("POST", "logout", apiLogoutParams)

    response = redirect(settings.BASEURL)
    response.delete_cookie("user_session")

    return response
