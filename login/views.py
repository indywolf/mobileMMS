import json
from django.http import HttpResponse
from mobileMMS.login.forms import LoginForm
from django.shortcuts import render
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
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
        print loginResponse
        print loginResponse["access_token"]
        print loginResponse["Customer"]["CustomerID"]


        response = render(request, 'loginresults.html', loginResponse)
        response.set_cookie("user_session", loginResponse["access_token"])
        response.set_cookie("user", loginResponse["Customer"]["CustomerID"])
        return response
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout(request):
    return render(request, 'login.html', {})
