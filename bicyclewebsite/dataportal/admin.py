from django.contrib import admin

# Register your models here.
from .models import RecordingSession, AudioInput, VideoInput

admin.site.register([RecordingSession,AudioInput,VideoInput])
