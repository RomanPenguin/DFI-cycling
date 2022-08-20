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
from .models import AudioInput, Empatica_EDA, RecordingSession,  VideoInput, AudioWords, Empatica_EDA, Empatica_TEMP, TextFile, GPS, HRV, Results, RawVideoInput, RawAudioInput, RawProcessingResults
from django.forms import ModelForm
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
import time, threading, mimetypes, os.path, os, shutil
from dataportal.generate_results import analysis
from dataportal.generate_raw_results import raw_analysis
from zipfile import ZipFile 

# default_save = '/home/tommy/Documents/output'
default_save = '/home/openface/Documents/output/'
sonixKeyFile = "/home/openface/Documents/sonixkey.txt"
dictionaryPath = 'Dictionary.txt'
#dictionaryPath = '/home/ubuntu/webserver/DFI-cycling/Dictionary.txt'
@login_required
def index(request):
    latest_session_list=RecordingSession.objects.order_by('-participantID')[:10]
    latest_raw_session_list = RawProcessingResults.objects.order_by('sessionID')[:10]
    status = {}
    raw_status = {}

    for session in latest_session_list:
        if os.path.exists(default_save + session.sessionID + "/" + session.sessionID + ".shp"):
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

    for session in latest_raw_session_list:
        if os.path.exists(default_save + session.sessionID+ '/' + session.sessionID + 'raw.zip'):
            newResults=Results(fileName = default_save + session.sessionID + '/' + session.sessionID + 'raw.zip')
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
            raw_status[session]='no results'
        else:
            raw_status[session]='results here'
                
    listLength=len(status)
    raw_listLength = len(raw_status)
    context={'latest_session_list':latest_session_list,'latest_raw_session_list': latest_raw_session_list, 'status':status,'raw_status':raw_status, 'listLength':listLength, 'raw_listLength': raw_listLength}
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
        empatica_EDA = session.empatica_EDA
    except session.empatica_EDA.DoesNotExist: 
        raise Http404("Empatica EDA file does not exist")
    
    try:
        empatica_TEMP = session.empatica_TEMP
    except session.empatica_TEMP.DoesNotExist: 
        raise Http404("Empatica TEMP file does not exist")

    try:
        textFile = session.textFile
    except session.textFile.DoesNotExist: 
        raise Http404("textfile file does not exist")

    try:
        gps = session.gPS
    except session.gPS.DoesNotExist: 
        raise Http404("gps file does not exist")

    try:
        results = session.results
    except session.results.DoesNotExist: 
        results = Results(fileNme='no results')

    return render(request, 'dataportal/detail.html', {'session': session, 'audioInput':audio, 'videoInput':video,'hRV':hrv, 'audioWords': audioWords, 'empatica_EDA':empatica_EDA, 'empatica_TEMP':empatica_TEMP, 'textFile':textFile, 'gPS':gps, 'results':results})
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
        empatica_EDAUpload=forms.FileField(allow_empty_file=True, required= False)
        empatica_TEMPUpload=forms.FileField(allow_empty_file=True, required= False)
        textFileUpload=forms.FileField(allow_empty_file=True, required= False)
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
                newEmpatica_EDAFile=Empatica_EDA(fileName=request.FILES['empatica_EDAUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['empatica_EDAUpload'])
                newEmpatica_EDAFile.save()
            except:
                newEmpatica_EDAFile = None
            
            try:
                newEmpatica_TEMPFile=Empatica_TEMP(fileName=request.FILES['empatica_TEMPUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['empatica_TEMPUpload'])
                newEmpatica_TEMPFile.save()
            except:
                newEmpatica_TEMPFile = None

            try:
                newTextFileFile=TextFile(fileName=request.FILES['textFileUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['textFileUpload'])
                newTextFileFile.save()
            except:
                newTextFileFile = None

            try:
                newGpsFile=GPS(fileName=request.FILES['gpsUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['gpsUpload'])
                newGpsFile.save()
            except:
                newGpsFile = None

            session=RecordingSession(sessionID=form.cleaned_data['sessionID'],participantID=form.cleaned_data['participantID'],audioInput=newAudioFile,videoInput=newVideoFile,hRV=newHrvFile,audioWords=newAudioWordsFile, empatica_EDA=newEmpatica_EDAFile,empatica_TEMP=newEmpatica_TEMPFile, textFile=newTextFileFile, gPS=newGpsFile)
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
    
    if not(os.path.isdir(default_save)):
        os.mkdir(default_save)
        print("default save location created")
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
            dictionaryPathFile = dictionaryPath
        except: 
            dictionaryPathFile = ''
        try:            
            hRVFile = session.hRV.media.path
        except:
            hRVFile = ''
        try:            
            empatica_EDAFile = session.empatica_EDA.media.path
        except:
            empatica_EDAFile = ''
        try:            
            empatica_TEMPFile = session.empatica_TEMP.media.path
        except:
            empatica_TEMPFile = ''
        try:            
            TextFileFile = session.textFile.media.path
        except:
            TextFileFile = ''
        inputFile= {
            'sessionID' : str(sessionID),
            'gps' : gpsFile,
            'emotions' : emotionsFile,
            'audio_sentences' : audioSentencesFile,
            'audio_words' : audioWordsFile,
            'dictionary_path' : dictionaryPathFile, # This path will be a constant
            'HRV_path' : hRVFile,
            'empatica_EDA': empatica_EDAFile,
            'empatica_TEMP': empatica_TEMPFile,
            'txt_file': TextFileFile
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
    
    def zip_write(zip, filename):
        zip.write(filename, os.path.basename(filename))

    if not(os.path.isfile(default_save+str(sessionID)+'/'+str(sessionID)+".zip")):

        z = ZipFile(default_save+str(sessionID)+'/'+str(sessionID)+'.zip', 'w')
        zip_write(z, default_save+str(sessionID)+'/'+str(sessionID)+'.dbf')
        zip_write(z, default_save+str(sessionID)+'/'+str(sessionID)+'.prj')
        zip_write(z, default_save+str(sessionID)+'/'+str(sessionID)+'.shp')
        zip_write(z, default_save+str(sessionID)+'/'+str(sessionID)+'.shx')
        z.close()

    fl_path = default_save+str(sessionID)+'/'+str(sessionID)+'.zip'
    filename = str(sessionID)+'.zip'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
def delete_results(request,sessionID): #delete folder with results
    
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

@login_required
def newRawSession(request): #upload new video/audio file for pre-processing


    class newRawSessionForm(forms.Form):
        rawVideoUpload=forms.FileField(allow_empty_file=True, required= False)
        rawAudioUpload=forms.FileField(allow_empty_file=True, required= False)
        

        sessionID=forms.CharField(max_length=100)
        
    
    if request.method == 'POST':
        form = newRawSessionForm(request.POST, request.FILES)
        
        if form.is_valid():
            if RecordingSession.objects.filter(sessionID=form.cleaned_data['sessionID']).exists():
                return HttpResponseForbidden("session already exists!")

            #use try statements 
            try:
                newRawAudioFile=RawAudioInput(fileName=request.FILES['rawAudioUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['rawAudioUpload'])
                newRawAudioFile.save()
            except: 
                newRawAudioFile = None
            try:
                newRawVideoFile=RawVideoInput(fileName=request.FILES['rawVideoUpload'].name,recordedTime=timezone.localtime(),media=request.FILES['rawVideoUpload'])
                newRawVideoFile.save()
            except:
                newRawVideoFile = None
           

            session=RawProcessingResults(sessionID=form.cleaned_data['sessionID'],rawVideoInput=newRawVideoFile, rawAudioInput=newRawAudioFile)
            session.save()
            return HttpResponseRedirect(reverse('dataportal:raw_detail', args=(form.cleaned_data['sessionID'],))) 
    else:
        form = newRawSessionForm()

    return render(request, "dataportal/new_raw_session.html", {
        "form": form,
        
        
    })

@login_required
def raw_detail(request, sessionID):
    try:
        rawSession = RawProcessingResults.objects.get(sessionID=sessionID)
        
    except RecordingSession.DoesNotExist:
        raise Http404("session does not exist")
    try:
        audio = rawSession.rawAudioInput
    except rawSession.rawAudioInput.DoesNotExist: 
        raise Http404("Audio file does not exist")

    try:
        video = rawSession.rawVideoInput
    except rawSession.rawVideoInput.DoesNotExist: 
        raise Http404("Audio file does not exist")

    
    try:
        results = rawSession.results
    except rawSession.results.DoesNotExist: 
        results = Results(fileNme='no results')

    return render(request, 'dataportal/raw_detail.html', {'session': rawSession, 'rawAudioInput':audio, 'rawVideoInput':video,'results':results})
    #return HttpResponse("You are looking at session %s" % sessionID)

@login_required
def generate_raw_results(request,sessionID):
    
    if not(os.path.isdir(default_save)):
        os.mkdir(default_save)
        print("default save location created")
    try:
        session = RawProcessingResults.objects.get(sessionID=sessionID) 
        try:
            rawAudioFile = session.rawAudioInput.media.path
        except:
            rawAudioFile=''
        try:     
            rawVideoFile = session.rawVideoInput.media.path
        except:
            rawVideoFile = ''
        
        inputFile= {
            'sessionID' : str(sessionID),
            'rawAudioFile' : rawAudioFile,
            'rawVideoFile' : rawVideoFile,
            
        }
        # t = threading.Thread(target=results_gen,args=[sessionID])
        t = threading.Thread(target=raw_analysis,args=[inputFile,default_save+str(sessionID),sonixKeyFile])
        
    except:
        return HttpResponseForbidden()
    t.setDaemon(True)
    t.start()
    return render(request, 'dataportal/generate_results.html')



@login_required
def download_raw_results(request,sessionID):
    
    fl_path = default_save+str(sessionID)+'/'+str(sessionID)+'raw.zip'
    filename = str(sessionID)+'raw.zip'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
def delete_raw_results(request,sessionID): #delete folder with results
    
    try:
        session=RawProcessingResults.objects.get(sessionID=sessionID)
    except:
        return HttpResponse("session does not exist")
    session.results=None
    session.save()
    try:
        fl_path = default_save+str(sessionID)+'/'+str(sessionID)+'raw.zip'
        os.remove(fl_path)
        fl_path = default_save+str(sessionID)+'/'+"words.csv"
        os.remove(fl_path)
        fl_path = default_save+str(sessionID)+'/'+'sentences.csv'
        os.remove(fl_path)



    except:
        return HttpResponse("file already deleted")

    return render(request, 'dataportal/delete_results.html')