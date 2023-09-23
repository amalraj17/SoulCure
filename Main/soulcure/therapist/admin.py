from django.contrib import admin
from .models import Therapy,Therapist,TherapistDayOff,LeaveRequest,TherapySessionSchedule

# Register your models here.
admin.site.register(Therapy)
admin.site.register(Therapist)
admin.site.register(TherapistDayOff)
admin.site.register(LeaveRequest)
admin.site.register(TherapySessionSchedule)