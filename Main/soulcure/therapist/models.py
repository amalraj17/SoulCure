from django.db import models
from accounts.models import CustomUser,UserProfile
from accounts.models import CustomUser, UserProfile
from client.models import Appointment


# Create your models here.
class Therapy(models.Model):
    therapy_name=models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=30)
    benefits = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.therapy_name 
    




class Therapist(models.Model):
    bio = models.TextField(blank=True, null=True)
    certification_name = models.CharField(max_length=50, blank=True)
    certificate_id = models.CharField(max_length=100, unique=True)
    experience = models.IntegerField(blank=True,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email




class Meeting(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)
    meeting_url = models.URLField()
    scheduled_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting for Appointment with {self.appointment.client.name} and {self.appointment.therapist.name} on {self.scheduled_time}"