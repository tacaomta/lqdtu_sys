from django.urls import path
from .views import overview_view, fields_view, roles_view, citations_view, performance_view, collaboration_view, upload_csv

urlpatterns = [
    path('', overview_view, name='overview'),
    path('fields/', fields_view, name='fields'),
    path('citations/', citations_view, name='citations'),
    path('roles/', roles_view, name='roles'),
    path('performance/', performance_view, name='performance'),
    path('collaboration/', collaboration_view, name='collaboration'),
    path('upload/', upload_csv, name='upload_csv'),
]