from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'segrez/index.html', context={})

