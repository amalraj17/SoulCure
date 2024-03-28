from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('addtherapy/',views.addTherapy,name='addTherapy'),
    # path('demo/',views.profile,name='demo'),
    path('demo2/',views.listTherapist,name='demo2'),
    path('listtherapist/',views.therapists,name='listtherapist'),
    path('familytherapist/',views.family_therapists,name='familytherapist'),
    path('change-password/',views.change_password,name='change_password'),
    path('therapist-profile/',views.therapistprofile,name='therapistProfile'),
    # path('tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    # path('therapist/tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    path('edit-therapist-profile/',views.edit_therapist_profile,name='edit-therapist-profile'),
    path('leave_request/',views.leave_request,name='leave_request'),
    path('schedule_therapy_session/<int:appointment_id>/', views.schedule_therapy_session, name='schedule_therapy_session'),
    path('fetch_appointments/', views.fetch_appointments, name='fetch_appointments'),
    path('view_therapy_schedules/', views.view_therapy_schedules, name='view_therapy_schedules'),
    path('view_therapy_schedule/<int:appointment_id>/', views.view_therapy_schedule, name='view_therapy_schedule'),


    path('view-therapist/<int:user_id>/',views.viewtherapist,name='view-therapist'),
    path('view-appointment-therapist/',views.view_appointment_therapist,name='view-appointment-therapist'),
    path('update-appointment-status/', views.update_appointment_status, name='update-appointment-status'),


]
