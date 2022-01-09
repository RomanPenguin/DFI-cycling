from django.contrib import admin

# Register your models here.
from .models import RecordingSession, AudioInput, VideoInput, HRV, SkinConductance, Fitbit, GPS

admin.site.register([RecordingSession,AudioInput,VideoInput, HRV, SkinConductance, Fitbit, GPS])
