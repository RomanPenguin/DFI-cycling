from django.contrib import admin

# Register your models here.
from .models import RecordingSession, AudioInput, VideoInput, HRV, AudioWords, Empatica_EDA, Empatica_TEMP, TextFile, GPS, RawVideoInput, RawAudioInput, RawProcessingResults

admin.site.register([RecordingSession,AudioInput,VideoInput, HRV, AudioWords, Empatica_EDA, Empatica_TEMP, TextFile, GPS, RawVideoInput, RawAudioInput, RawProcessingResults])
