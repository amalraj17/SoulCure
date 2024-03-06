from django.contrib import admin

from .models import Room,Message,UserRooms,Notification

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserRooms)
admin.site.register(Notification)