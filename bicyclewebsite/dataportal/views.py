from email.policy import default
from typing import NamedTuple
from django import http
from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
# Create your views here.
from django.views import generic 
from django.urls import reverse
from django.http import HttpResponse
from django.utils.translation import templatize
from django import forms 
from .models import AudioInput, RecordingSession,  VideoInput, AudioWords, Fitbit, GPS, HRV, Results
from django.forms import ModelForm
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
import time, threading, mimetypes, os.path, os, shutil
from dataportal.generate_results import analysis


default_save = '/home/openface/Documents/new_cycling/DFI-cycling/output/allresults/'

@login_required
def index(request):
    latest_session_list=RecordingSession.objects.order_by('-participantID')[:5]
    
    status = {}
    
    for session in latest_session_list:
        if os.path.isdir(default_save + session.sessionID):
            newResults=Results(fileName = default_save + session.sessionID + '/' + session.sessionID + '.zip')
            newResults.save()
            session.results = newResults
            session.save()
        else:
            print ("File not exist")
            
        

        try:
            check = session.results
        except Results.DoesNotExist:
            raise Http404("session does not exist")
        if check == None:  
            status[session]='no results'
        else:
            status[session]='results here'
                
    listLength=len(status)
    context={'latest_session_list':latest_session_list,'status':status,'listLength':listLength}
    #return HttpResponse(template.render(context,request))
    return render(request, 'dataportal/index.html', context)

@login_required
def detail(request, sessionID):
    try:
        session = RecordingSession.objects.get(sessionID=sessionID)
        
    except RecordingSession.DoesNotExist:
        raise Http404("session does not exist")
    try:
        audio = session.audioInput
    except session.audioInput.DoesNotExist: 
        raise Http404("Audio file does not exist")

    try:
        video = session.videoInput
    except session.videoInput.DoesNotExist: 
        raise Http404("Audio file does not exist")

    try:
        hrv = session.hRV
    except session.hRV.DoesNotExist: 
        raise Http404("HRV file does not exist")

    try:
        audioWords = session.audioWords
    except session.audioWords.DoesNotExist: 
        raise Http404("audio words file does not exist")

    try:
        fitbit = session.fitbit
    except session.fitbit.DoesNotExist: 
        raise Http404("fitbit file does not exist")

    try:
        gps = session.gPS
    except session.gPS.DoesNotExist: 
        raise Http404("gps file does not exist")

    try:
        results = session.results
    except session.results.DoesNotExist: 
        results = Results(fileNme='no results')

    return render(request, 'dataportal/detail.html', {'session': session, 'audioInput':audio, 'videoInput':video,'hRV':hrv, 'audioWords': audioWords, 'fitbit':fitbit, 'gPS':gps, 'results':results})
    #return HttpResponse("You are looking at session %s" % sessionID)

@login_required
def upload(request,sessionID): #not used for now
    class UploadForm(forms.Form):
        videoUpload=forms.FileField(allow_empty_file=True)
        audioUpload=forms.FileField(allow_empty_file=True)
        nameTest=forms.CharField(max_length=100)

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            session = RecordingSession.objects.get(sessionID=sessionID)
            newAudioFile=AudioInput(fileName=request.FILES['audioUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['audioUpload'])
            newVideoFile=VideoInput(fileName=request.FILES['videoUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['videoUpload'])
            newAudioFile.save()
            newVideoFile.save()
            session.audioInput = newAudioFile
            session.videoInput = newVideoFile
            session.save()
            print("success")
            return HttpResponseRedirect(reverse('dataportal:detail', args=(sessionID,))) 
    else:
        form = UploadForm()

    return render(request, "dataportal/upload.html", {
        "form": form,
        "sessionID": sessionID
        
    })

@login_required
def newSession(request):
    class newSessionForm(forms.Form):
        videoUpload=forms.FileField(allow_empty_file=True, required= False)
        audioUpload=forms.FileField(allow_empty_file=True, required= False)
        hrvUpload=forms.FileField(allow_empty_file=True, required= False)
        audioWordsUpload=forms.FileField(allow_empty_file=True, required= False)
        fitbitUpload=forms.FileField(allow_empty_file=True, required= False)
        gpsUpload=forms.FileField(allow_empty_file=True, required= False)

        sessionID=forms.CharField(max_length=100)
        participantID=forms.CharField(max_length=100)
    
    if request.method == 'POST':
        form = newSessionForm(request.POST, request.FILES)
        
        if form.is_valid():
            if RecordingSession.objects.filter(sessionID=form.cleaned_data['sessionID']).exists():
                return HttpResponseForbidden("session already exists!")

            #use try statements 
            try:
                newAudioFile=AudioInput(fileName=request.FILES['audioUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['audioUpload'])
                newAudioFile.save()
            except: 
                newAudioFile = None
            try:
                newVideoFile=VideoInput(fileName=request.FILES['videoUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['videoUpload'])
                newVideoFile.save()
            except:
                newVideoFile = None
            try:
                newHrvFile=HRV(fileName=request.FILES['hrvUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['hrvUpload'])
                newHrvFile.save()
            except:
                newHrvFile = None
            try:
                newAudioWordsFile=AudioWords(fileName=request.FILES['audioWordsUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['audioWordsUpload'])
                newAudioWordsFile.save()
            except:
                newAudioFile = None
            try:
                newFitbitFile=Fitbit(fileName=request.FILES['fitbitUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['fitbitUpload'])
                newFitbitFile.save()
            except:
                newFitbitFile = None
            try:
                newGpsFile=GPS(fileName=request.FILES['gpsUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['gpsUpload'])
                newGpsFile.save()
            except:
                newGpsFile = None

            session=RecordingSession(sessionID=form.cleaned_data['sessionID'],participantID=form.cleaned_data['participantID'],audioInput=newAudioFile,videoInput=newVideoFile,hRV=newHrvFile,audioWords=newAudioWordsFile, fitbit=newFitbitFile, gPS=newGpsFile)
            session.save()
            return HttpResponseRedirect(reverse('dataportal:detail', args=(form.cleaned_data['sessionID'],))) 
    else:
        form = newSessionForm()

    return render(request, "dataportal/new_session.html", {
        "form": form,
        
        
    })

# def results_gen(sessionID):
    
#     session=RecordingSession.objects.get(sessionID=sessionID)
#     session.results=Results(fileName="testing")
#     time.sleep(10)
#     session.results.save()
#     session.save()




@login_required
def generate_results(request,sessionID):
    
    try:
        session = RecordingSession.objects.get(sessionID=sessionID) 
        try:
            gpsFile = session.gPS.media.path
        except:
            gpsFile=''
        try:     
            emotionsFile = session.videoInput.media.path
        except:
            emotionsFile = ''
        try:
            audioSentencesFile = session.audioInput.media.path
        except:
            audioSentencesFile = ''
        try:
            audioWordsFile = session.audioWords.media.path
        except:
            audioWordsFile = ''
        try:
            dictionaryPathFile = 'Dictionary.txt'
        except: 
            dictionaryPathFile = ''
        try:            
            hRVFile = session.hRV.media.path
        except:
            hRVFile = ''
        inputFile= {
            'sessionID' : str(sessionID),
            'gps' : gpsFile,
            'emotions' : emotionsFile,
            'audio_sentences' : audioSentencesFile,
            'audio_words' : audioWordsFile,
            'dictionary_path' : dictionaryPathFile, # This path will be a constant
            'HRV_path' : hRVFile
        }
        # t = threading.Thread(target=results_gen,args=[sessionID])
        t = threading.Thread(target=analysis,args=[inputFile,default_save+str(sessionID)])
        
    except:
        return HttpResponseForbidden()
    t.setDaemon(True)
    t.start()
    return render(request, 'dataportal/generate_results.html')


@login_required
def download_results(request,sessionID):
    
    fl_path = default_save+str(sessionID)+'/'+str(sessionID)+'.zip'
    filename = str(sessionID)+'.zip'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
def delete_results(request,sessionID):
    
    try:
        session=RecordingSession.objects.get(sessionID=sessionID)
    except:
        return HttpResponse("session does not exist")
    session.results=None
    session.save()
    try:
        fl_path = default_save+str(sessionID)
        shutil.rmtree(fl_path)

    except:
        return HttpResponse("file already deleted")

    return render(request, 'dataportal/delete_results.html')



