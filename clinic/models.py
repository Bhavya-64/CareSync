import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    expiry_date = models.DateField()

class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_profile'
    )

    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    available_today = models.BooleanField(default=True)
    available_time = models.CharField(max_length=100)
    

class Appointment(models.Model):
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class VirtualAssistance(models.Model):
    problem = models.CharField(max_length=200)
    first_aid = models.TextField()

class EmergencyRequest(models.Model):

    CONSULTATION_CHOICES = [
        ('video', 'Video Consultation'),
        ('chat', 'Chat'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15, blank=True)
    symptoms = models.TextField()

    consultation_type = models.CharField(
        max_length=10,
        choices=CONSULTATION_CHOICES,
        default='video'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_requests'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    room_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.status}"
user = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='doctor_profile'
)