from django.urls import path, include
from .views import *


app_name = 'autosegmentation'

urlpatterns = [
    path('', autoSegmentation, name='auto'),
]
