from django.db import models
from datetime import datetime
from accounts.models import CustomUser


class Appointment(models.Model):
    TIME_CHOICES = [
        (datetime.strptime('09:00 AM', '%I:%M %p').time(), '09:00 AM'),
        (datetime.strptime('11:00 AM', '%I:%M %p').time(), '11:00 AM'),
        (datetime.strptime('01:00 PM', '%I:%M %p').time(), '01:00 PM'),
        (datetime.strptime('03:00 PM', '%I:%M %p').time(), '03:00 PM'),
        (datetime.strptime('05:00 PM', '%I:%M %p').time(), '05:00 PM'),
    ]

    STATUS_CHOICES = [
        ("not_paid", "Not_paid"),
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]

    date = models.DateField()
    client = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='client_appointments',
        limit_choices_to={'role': CustomUser.CLIENT}
    )
    therapist = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, 
        related_name='therapist_appointments',
        limit_choices_to={'role': CustomUser.THERAPIST}
    )
    time_slot = models.TimeField(choices=TIME_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_paid')
    order_id = models.CharField(max_length=100, blank=True, null=True)



 
    def __str__(self):
        return f"Appointment with {self.client.name} and {self.therapist.name} on {self.date} at {self.get_time_slot_display()}"
