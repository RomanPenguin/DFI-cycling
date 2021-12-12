from django.db import models
from awstranscription.models import RecordingSession, AudioInput, VideoInput
from django.utils import timezone
r1=AudioInput(fileName="audiotest1.mp3",recordedTime=timezone.localtime())
r2=VideoInput(filename='videotest.mp4',recordedTime=timezone.localtime())
r3=RecordingSession(sessionID=1,participantID=2,audioInput=r1,videoInput=r2)