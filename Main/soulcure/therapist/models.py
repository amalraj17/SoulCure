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






from django.db import models
from datetime import datetime
from accounts.models import CustomUser

class TherapySession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    appointment = models.OneToOneField(Appointment,on_delete=models.CASCADE,related_name='therapy_session',null=True,blank=True)
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    meeting_link = models.URLField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Therapy Session with {self.appointment.client.name} and {self.appointment.therapist.name} on {self.scheduled_datetime}"

    class Meta:
        ordering = ['scheduled_datetime']




class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    therapist = models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role': 2})
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def str(self):
        return f'{self.therapist.name} - {self.date} ({self.status})'
    

class TherapistDayOff(models.Model):
    therapist = models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role': 2})
    date = models.DateField()

    def str(self):
        return f"{self.therapist.name} - {self.date}"