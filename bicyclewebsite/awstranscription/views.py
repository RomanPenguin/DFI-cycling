from django import http
from django.shortcuts import render
from django.template import loader
from django.http import Http404
# Create your views here.
from django.views import generic 
from django.urls import reverse
from django.http import HttpResponse
from django.utils.translation import templatize

from .models import RecordingSession


def index(request):
    latest_session_list=RecordingSession.objects.order_by('-participantID')[:5]
    context={'latest_session_list':latest_session_list,}
    #return HttpResponse(template.render(context,request))
    return render(request, 'awstranscription/index.html', context)

def detail(request, sessionID):
    try:
        session = RecordingSession.objects.get(sessionID=sessionID)
    except RecordingSession.DoesNotExist:
        raise Http404("session does not exist")
    return render(request, 'awstranscription/detail.html', {'session': session})
    #return HttpResponse("You are looking at session %s" % sessionID)

def upload(request, sessionID):
    return HttpResponse("you are looking at the upload page for session %s" % sessionID)

