from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    print(request.META)
    return HttpResponse('Goodbye World')


def test(request):
    print(request.META)
    return HttpResponse('Test Page')
