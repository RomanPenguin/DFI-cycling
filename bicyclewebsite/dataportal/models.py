from django.db import models
from django.db.models.base import Model
import datetime 
from django.utils import timezone
# Create your models here.
    
class AudioInput(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession=models.OneToOneField(RecordingSession,on_delete=models.CASCADE)
    media = models.FileField(upload_to='media',null=True, blank=True)    
    def __str__(self):
        return self.fileName


class VideoInput(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class HRV(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class AudioWords(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class Empatica_EDA(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName


class Empatica_TEMP(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class TextFile(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class GPS(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class GPX(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class Results(models.Model):
    fileName=models.CharField(max_length=200)
    #recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    #media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class RecordingSession(models.Model):
    sessionID=models.CharField(max_length=200)
    participantID=models.CharField(max_length=200)
    audioInput=models.OneToOneField(AudioInput,on_delete=models.CASCADE,null=True,blank=True)
    videoInput=models.OneToOneField(VideoInput,on_delete=models.CASCADE,null=True,blank=True)
    hRV=models.OneToOneField(HRV,on_delete=models.CASCADE,null=True,blank=True)
    audioWords=models.OneToOneField(AudioWords,on_delete=models.CASCADE,null=True,blank=True)
    empatica_EDA=models.OneToOneField(Empatica_EDA,on_delete=models.CASCADE,null=True,blank=True)
    empatica_TEMP=models.OneToOneField(Empatica_TEMP,on_delete=models.CASCADE,null=True,blank=True)
    textFile=models.OneToOneField(TextFile,on_delete=models.CASCADE,null=True,blank=True)
    gPS=models.OneToOneField(GPS,on_delete=models.CASCADE,null=True,blank=True)
    gPX=models.OneToOneField(GPX,on_delete=models.CASCADE,null=True,blank=True)

    results=models.OneToOneField(Results,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.sessionID


#pre-processing files (raw video file -> emotion)
class RawVideoInput(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

#pre-processing files (raw audio file -> transcription)
class RawAudioInput (models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class RawProcessingResults(models.Model):
    sessionID=models.CharField(max_length=200)
    rawVideoInput=models.OneToOneField(RawVideoInput,on_delete=models.CASCADE,null=True,blank=True)
    rawAudioInput=models.OneToOneField(RawAudioInput,on_delete=models.CASCADE,null=True,blank=True)
    results=models.OneToOneField(Results,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.sessionID

