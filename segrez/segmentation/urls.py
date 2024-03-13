from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='segmentation.index'),
    path('test/', test, name='testDraw'),
    path('upload/', FileFieldFormView.as_view(), name='upload_images'),
    path('test/get_image_name/', get_image_name, name='get_image_name'),
    path('test/get_tag/', get_tag, name='get_tag'),
    path('test/save_data/', save_data, name='save_data')
]
