from django.db import models
from datetime import datetime
from accounts.models import CustomUser
from django.utils import timezone


class Appointment(models.Model):
    TIME_CHOICES = [
        (datetime.strptime('09:00 AM', '%I:%M %p').time(), '09:00 AM'),
        (datetime.strptime('11:00 AM', '%I:%M %p').time(), '11:00 AM'),
        (datetime.strptime('01:00 PM', '%I:%M %p').time(), '01:00 PM'),
        (datetime.strptime('03:00 PM', '%I:%M %p').time(), '03:00 PM'),
        (datetime.strptime('05:00 PM', '%I:%M %p').time(), '05:00 PM'),
    ]

    STATUS_CHOICES = [
        ("not_paid", "Not Paid"),
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled','Cancelled'),
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
    time_slot = models.TimeField(choices=TIME_CHOICES,null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_paid')
    payment_status= models.BooleanField(default=True)
    cancel_status=models.BooleanField(default=False)




    def __str__(self):
        return f"Appointment with {self.client.name} and {self.therapist.name} on {self.date} at {self.get_time_slot_display()}"
    def save(self, *args, **kwargs):
        if self.payment_status == False:
            # Set the time_slot field to None when status is 'not_paid'
            self.time_slot = None
        super(Appointment, self).save(*args, **kwargs)




class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    

        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
    razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
    payment_id = models.CharField(max_length=255)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=5)  # Currency code (e.g., "INR")
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)


    def __str__(self):
        return f"Payment for {self.appointment}"



    class Meta:
        ordering = ['-timestamp']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()
