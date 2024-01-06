from django.shortcuts import render
from django.http import HttpResponse

from .models import Tags


def index(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/index.html', {'tags': tags, 'title': 'Список тегов'})


def test(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/testDraw.html', {'tags': tags, 'title': 'Test Draw'})
