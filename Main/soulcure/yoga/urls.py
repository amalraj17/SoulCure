from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('yoga/',views.yoga_page,name='yoga'),
    path('yoga_instructions/',views.yoga_instructions,name='yoga_instructions'),
    path('inf', views.inf, name='inf'),
]
