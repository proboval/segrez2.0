from django.urls import path
from .views import *


app_name = 'segmentation'

urlpatterns = [
    path('', index, name='segmentation.index'),
    path('tests/', test, name='testDraw'),
    path('upload/project/', upload_project, name='upload_project'),
    path('upload/', upload_show, name='upload'),
    path('upload/save_change_tag/', change_tag, name='change_tag'),
    path('changeProject/delete_tag/', delete_tag, name='delete_tag'),
    path('upload/get_tag/', get_tag, name='get_tag'),
    path('upload/save_new_tag/', save_new_tag, name='save_new_tag'),
    path('tests/save_polygon/', save_polygon, name='save_polygon'),
    path('tests/del_polygon/', del_polygon, name='del_polygon'),
    path('projects/', project_show, name='project_show'),
    path('changeProject/', changeProject, name='changeProject'),
    path('changeProject/deleteImage/', deleteImage, name='deleteImage'),
    path('changeProject/deleteProject/', deleteProject, name='deleteProject'),
    path('changeProject/project/', changeProjectData, name='changeProjectData'),
]
