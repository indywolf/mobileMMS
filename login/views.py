from django.shortcuts import redirect
from mobileMMS.login.forms import LoginForm
from mobileMMS.login.forms import ForgotForm
from django.shortcuts import render
from mobileMMS.CustomerAPI.customerAPI import CustomerAPI
from mobileMMS.utilities.common import getEncryptedValue
from mobileMMS.utilities.common import getDecryptedValue
from django.conf import settings
from mobileMMS.utilities.common import getSessionToken



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

            if loginResponse["error"] == "invalid_client":
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'error' : 'Please enter a valid username/password'})
            else:
                response = render(request, 'loginresults.html', loginResponse)
                print 'valid response'
                response.set_cookie("user_session", getEncryptedValue(loginResponse["access_token"]), max_age=1209600)
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

def forgot(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            apiForgotParams = {
                "Email": cd["Email"],
                "Firstname": cd["FirstName"],
                "LocationID": settings.APILOCATION,
                "BrandID": None,
                "access_token": getSessionToken(request)
            }

            cs = CustomerAPI()
            forgotResponse = cs.request("POST","forgot_password", apiForgotParams)
            print forgotResponse
            if forgotResponse["ErrorCode"] != 0:
                form = ForgotForm()
                return render(request, 'forgot.html', {'form': form, 'error' : forgotResponse["ErrorMessage"]})
            else:
                print 'valid response'
                response = render(request, 'forgotresults.html', apiForgotParams)
                return response
    else:
        form = ForgotForm()
        return render(request, 'forgot.html', {'form': form})
