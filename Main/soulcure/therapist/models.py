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




# class Meeting(models.Model):
#     PLATFORM_CHOICES = [
#         ('Platform1', 'Platform 1'),
#         ('Platform2', 'Platform 2'),
#         ('Platform3', 'Platform 3'),
#     ]

#     STATUS_CHOICES = [
#         ('scheduled', 'Scheduled'),
#         ('confirmed', 'Confirmed'),
#         ('completed', 'Completed'),
#     ]

#     appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
#     client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_meetings')
#     therapist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='therapist_meetings')
#     platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
#     meeting_url = models.URLField()
#     scheduled_time = models.DateTimeField()
#     duration_minutes = models.PositiveIntegerField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             # This is a new Meeting, so let's copy data from the associated Appointment
#             self.client = self.appointment.client
#             self.therapist = self.appointment.therapist
#             self.scheduled_time = self.appointment.date + self.appointment.time_slot
#             self.duration_minutes = 60  # Set an initial duration (adjust as needed)
#         super(Meeting, self).save(*args, **kwargs)



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