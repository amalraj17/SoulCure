
from django.db import models
from accounts.models import CustomUser

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name
class Notifiction(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content=models.CharField(max_length=1000)
    time=models.DateTimeField()

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return f"chat of {self.user.name} in {self.room.name} on {self.date_added}"

class UserRooms(models.Model):
    room = models.ForeignKey(Room, related_name='userrooms', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='userrooms', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    in_check = models.BooleanField(default=False)
    def __str__(self):
        return self.room.name