from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    if "user_session" in request.COOKIES and "user" in request.COOKIES:
        headerstatus = { "message": "logged in"}
    else:
        headerstatus = { "message": "anonymous"}

    return render(request, 'home.html', headerstatus)
