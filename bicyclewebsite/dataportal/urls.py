from django.urls import path
from django.conf.urls import include, url
from . import views

app_name='dataportal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sessionID>/',views.detail, name='detail'),
    path('raw/<int:sessionID>/',views.raw_detail, name='raw_detail'),
    path('<int:sessionID>/upload/',views.upload,name='upload'),
    path('new_session/',views.newSession,name='newSession'),
    path('new_raw_session/',views.newRawSession,name='new_raw_session'),
    path('generate_results/<int:sessionID>/',views.generate_results,name='generate_results'),
    path('generate_raw_results/<int:sessionID>/',views.generate_raw_results,name='generate_raw_results'),
    path('download_results/<int:sessionID>/',views.download_results,name='download_results'),
    path('download_raw_results/<int:sessionID>/',views.download_raw_results,name='download_raw_results'),
    path('delete_results/<int:sessionID>/',views.delete_results,name='delete_results'),
]