from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('meeting/client/',views.videocallclient, name='meetingclient'),
    path('join/<int:roomID>/<int:appointment_id>/',views.join_room, name='join_room'),
    ]