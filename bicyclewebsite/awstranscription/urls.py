from django.urls import path

from . import views

app_name='awstranscription'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sessionID>/',views.detail, name='detail'),
    path('<int:sessionID>/upload/',views.upload,name='upload'),
    path('new_session/',views.newSession,name='newSession')

]