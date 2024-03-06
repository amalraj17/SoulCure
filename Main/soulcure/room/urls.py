from django.urls import path

from . import views


urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('room/<slug:slug>/', views.room, name='room'),
    path('notification/', views.notification, name='notification'),
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]