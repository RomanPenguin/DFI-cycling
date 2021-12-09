from django import http
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponseRedirect
# Create your views here.
from django.views import generic 
from django.urls import reverse
from django.http import HttpResponse
from django.utils.translation import templatize
from django import forms 
from .models import AudioInput, RecordingSession
from django.forms import ModelForm

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

def upload(request,sessionID):
    class UploadForm(ModelForm):
        class Meta:
            model = AudioInput
            fields = '__all__'

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('awstranscription:detail', args=(sessionID,))) 
    else:
        form = UploadForm()

    return render(request, "awstranscription/upload.html", {
        "form": form,
        "sessionID": sessionID
        
    })
    return HttpResponse("you are looking at the upload page for session %s" % sessionID)

