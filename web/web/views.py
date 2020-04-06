from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return HttpResponseRedirect("/goldennum")


def favicon(request):
    return HttpResponseRedirect("https://storage.jbesu.com/goldennum/favicon.ico")
