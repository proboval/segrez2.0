from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('logout/', logout_user, name='logout_user'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('segmentation/', include('segmentation.urls')),
]
