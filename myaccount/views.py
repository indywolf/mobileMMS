from django.shortcuts import render
from django.shortcuts import redirect
from mobileMMS.myaccount.forms import UpdateAccountForm
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from mobileMMS.utilities.common import getSessionToken
from django.conf import settings

def updateAccount(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST)
        if form.is_valid():

            accessToken = getSessionToken(request)
            print 'access token: ' + accessToken

            cd = form.cleaned_data
            updateAccountData = {
                "Address": {
                    "City": cd['City'],
                    "Country": {
                        "ID": 1,
                        "Name": ""
                    },
                    "State": cd['State'],
                    "Street1": cd['Street1'],
                    "Street2": cd['Street2'],
                    "Zip": cd['ZipCode']
                },
                "AllowReceiveEmails": cd['AllowReceiveEmails'],
                "AllowReceiveSMS": cd['AllowReceiveSMS'],
                "CellPhone": cd['CellPhone'],
                "Email": cd['Email'],
                "FirstName": cd['FirstName'],
                "GUID": "",
                "HomePhone": cd['HomePhone'],
                "LastName": cd['LastName'],
                "LocationID": settings.APILOCATION,
                "OriginationID": None,
                "WorkPhone": cd['WorkPhone'],
                "access_token": accessToken
            }

            cs = CustomerAPI()
            customerResponse = cs.request("POST","customer/account", updateAccountData)
            print customerResponse
            if customerResponse["IsSuccess"] is True:
                response = redirect(settings.BASEURL + "/login")
                response.set_cookie("location_id", settings.APILOCATION, )
                return response
            else:
                print customerResponse
                return render(request, 'register_form.html', {'form': form, "error": customerResponse["ErrorMessage"]})

    else:
        if "user_session" in request.COOKIES and "user" in request.COOKIES:
            form = UpdateAccountForm()
            return render(request, 'myaccount_form.html', {'form': form})
        else:
            response = redirect(settings.BASEURL + '/login/')
            return response

