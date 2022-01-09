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

class SkinConductance(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    #recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.fileName

class Fitbit(models.Model):
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

class RecordingSession(models.Model):
    sessionID=models.CharField(max_length=200)
    participantID=models.CharField(max_length=200)
    audioInput=models.OneToOneField(AudioInput,on_delete=models.CASCADE)
    videoInput=models.OneToOneField(VideoInput,on_delete=models.CASCADE)
    hRV=models.OneToOneField(HRV,on_delete=models.CASCADE)
    skinConductance=models.OneToOneField(SkinConductance,on_delete=models.CASCADE)
    fitbit=models.OneToOneField(Fitbit,on_delete=models.CASCADE)
    gPS=models.OneToOneField(GPS,on_delete=models.CASCADE)
    def __str__(self):
        return self.sessionID

