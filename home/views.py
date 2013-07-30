from django.shortcuts import render
from mobileMMS.utilities.common import getSessionDictionary

def home(request):
    sessioninfo = getSessionDictionary(request)

    return render(request, 'home.html', sessioninfo)
