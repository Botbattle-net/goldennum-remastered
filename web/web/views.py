from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return HttpResponseRedirect("/goldennum")
