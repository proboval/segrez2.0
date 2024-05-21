from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('logout/', logout_user, name='logout_user'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('segmentation/', include('segmentation.urls')),
    path('checkCode/', checkCode_view, name='checkCode'),
    path('checkCode/cancel/', cancelRegistration, name='cancelRegistration'),
    path('addUser/', addUser, name='addUser'),
    path('removeExpertFromCompany/', removeExpertFromCompany, name='removeExpertFromCompany')
]
