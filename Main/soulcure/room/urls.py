from django.urls import path

from . import views


urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('room/<slug:slug>/', views.room, name='room'),
    path('notification/<slug:slug>/', views.notification, name='notification'),
    path('mark_notifications_as_read/<slug:slug>/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    
]