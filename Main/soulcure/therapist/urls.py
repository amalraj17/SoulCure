from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('addtherapy/',views.addTherapy,name='addTherapy'),
    # path('demo/',views.profile,name='demo'),
    path('demo2/',views.listTherapist,name='demo2'),
]
