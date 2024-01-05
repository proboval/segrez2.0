from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='segmentation.index'),
    path('test/', test)
]
