from django.urls import path
from django.conf.urls import include, url
from . import views

app_name='dataportal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sessionID>/',views.detail, name='detail'),
    path('<int:sessionID>/upload/',views.upload,name='upload'),
    path('new_session/',views.newSession,name='newSession'),
    path('generate_results/<int:sessionID>/',views.generate_results,name='generate_results'),
    path('download_results/<int:sessionID>/',views.download_results,name='download_results'),

    path('delete_results/<int:sessionID>/',views.delete_results,name='delete_results'),
]