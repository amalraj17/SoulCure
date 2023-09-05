from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('addtherapy/',views.addTherapy,name='addTherapy'),
    # path('demo/',views.profile,name='demo'),
    path('demo2/',views.listTherapist,name='demo2'),

    path('change-password/',views.change_password,name='change_password'),
    path('therapist-profile/',views.therapistprofile,name='therapistProfile'),
    path('tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    # path('therapist/tprofile/<int:therapist_id>/', views.therapist_profile, name='tprofile'),
    path('edit-therapist-profile/',views.edit_therapist_profile,name='edit-therapist-profile'),
 

]
