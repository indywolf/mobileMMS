from django.shortcuts import render
from django.shortcuts import redirect
from mobileMMS.myaccount.forms import EditAccountForm
from mobileMMS.myaccount.forms import UpdatePasswordForm
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from mobileMMS.utilities.common import getSessionToken
from mobileMMS.utilities.common import getSessionDictionary
from django.conf import settings


def myAccount(request):
    session = getSessionDictionary(request)
    if 'user_session' in session:
        return render(request, 'myaccount.html', session)
    else:
        response = redirect(settings.BASEURL + '/login/')
        return response

def updatePassword(request):
    session = getSessionDictionary(request)
    if 'user_session' not in session:
        response = redirect(settings.BASEURL + '/login/')
        return response
    else:
        if request.method == 'POST':
            form = UpdatePasswordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                updatePasswordData = {
                    "CustomerID": session['user'],
                    "Email": cd['Email'],
                    "LocationID": settings.APILOCATION,
                    "NewPassword": cd['NewPassword'],
                    "OldPassword": cd['OldPassword'],
                    "access_token": getSessionToken(request)
                }
                cs = CustomerAPI()
                customerResponse = cs.request("POST","customer/password", updatePasswordData)
                print customerResponse
                if customerResponse["IsSuccess"] is True:
                    response = redirect(settings.BASEURL + "/myaccount/")
                    response.set_cookie("location_id", settings.APILOCATION, )
                    return response
                else:
                    print customerResponse
                    return render(request, 'updatepassword.html', {'form': form, "error": customerResponse["ErrorMessage"]})
        else:
            form = UpdatePasswordForm()
            return render(request, 'updatepassword.html', {'form': form})

def editAccount(request):
    session = getSessionDictionary(request)
    if 'user_session' not in session:
        response = redirect(settings.BASEURL + '/login/')
        return response
    else:
        if request.method == 'POST':
            form = EditAccountForm(request.POST)
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
                customerResponse = cs.request("PUT","customer/" + session['user'], updateAccountData)
                print customerResponse
                if customerResponse["IsSuccess"] is True:
                    response = redirect(settings.BASEURL + "/myaccount/")
                    response.set_cookie("location_id", settings.APILOCATION, )
                    return response
                else:
                    print customerResponse
                    return render(request, 'editaccount.html', {'form': form, "error": customerResponse["ErrorMessage"]})

        else:
            getCustomerData = { 'access_token' : getSessionToken(request)}
            cs = CustomerAPI()
            customerResponse = cs.request("GET","customer/" + session['user'], getCustomerData)
            print customerResponse
            userData = customerResponse['Customer']['Customer']
            current = {
                "Email" : userData['Email'],
                'FirstName' : userData['FirstName'],
                'LastName' : userData['LastName'],
                'HomePhone' : userData['HomePhone'],
                'CellPhone' : userData['CellPhone'],
                'WorkPhone' : userData['WorkPhone'],
                'AllowReceiveEmails' : userData['AllowReceiveEmails'],
                'AllowReceiveSMS' : userData['AllowReceiveSMS'],
                'Street1' : userData['Address']['Street1'],
                'Street2' : userData['Address']['Street2'],
                'City' : userData['Address']['City'],
                'State' : userData['Address']['State'],
                'ZipCode' : userData['Address']['Zip']
            }

            f = EditAccountForm(initial=current)
            return render(request, "editaccount.html", {'form': f})

