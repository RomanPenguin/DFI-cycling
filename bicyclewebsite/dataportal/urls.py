from django.urls import path
from django.conf.urls import include, url
from . import views

app_name='dataportal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sessionID>/',views.detail, name='detail'),
    path('<int:sessionID>/upload/',views.upload,name='upload'),
    path('new_session/',views.newSession,name='newSession'),
]