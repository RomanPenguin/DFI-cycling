from django.db import models
from django.db.models.base import Model
import datetime 
from django.utils import timezone
# Create your models here.

class RecordingSession(models.Model):
    sessionID=models.CharField(max_length=200)
    participantID=models.CharField(max_length=200)
    def __str__(self):
        return self.sessionID
    
    def __iter__(self):
       ''' Returns the Iterator object '''
       return RecordingSession(self)
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class AudioInput(models.Model):
    fileName=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    recordingSession=models.OneToOneField(RecordingSession,on_delete=models.CASCADE)
    media = models.FileField(upload_to='media',null=True, blank=True)    
    def __str__(self):
        return self.fileName


class VideoInput(models.Model):
    filename=models.CharField(max_length=200)
    recordedTime=models.DateTimeField('date recorded')
    recordingSession= models.OneToOneField(RecordingSession, on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", null=True, blank=True)      
    def __str__(self):
        return self.filename

