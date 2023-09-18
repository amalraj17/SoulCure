from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('addtherapy/',views.addTherapy,name='addTherapy'),
    # path('demo/',views.profile,name='demo'),
    path('demo2/',views.listTherapist,name='demo2'),
    path('listtherapist/',views.therapists,name='listtherapist'),
    path('change-password/',views.change_password,name='change_password'),
    path('therapist-profile/',views.therapistprofile,name='therapistProfile'),
    path('tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    # path('therapist/tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    path('edit-therapist-profile/',views.edit_therapist_profile,name='edit-therapist-profile'),

    path('view-therapist/<int:user_id>/',views.viewtherapist,name='view-therapist'),
    path('view-appointment-therapist/',views.view_appointment_therapist,name='view-appointment-therapist'),
    path('update-appointment-status/', views.update_appointment_status, name='update-appointment-status'),


 

]
