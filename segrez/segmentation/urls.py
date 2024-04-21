from django.urls import path
from .views import *


app_name = 'segmentation'

urlpatterns = [
    path('', index, name='segmentation.index'),
    path('test/', test, name='testDraw'),
    path('upload/', FileFieldFormView.as_view(), name='upload_images'),
    path('upload/save_change_tag/', change_tag, name='change_tag'),
    path('upload/delete_tag/', delete_tag, name='delete_tag'),
    path('test/get_image_name/', get_image_name, name='get_image_name'),
    path('upload/get_tag/', get_tag, name='get_tag'),
    path('upload/save_new_tag/', save_new_tag, name='save_new_tag'),
    path('test/save_polygon/', save_polygon, name='save_polygon'),
    path('test/del_polygon/', del_polygon, name='del_polygon'),
    path('projects/', project_show, name='project_show'),
]
