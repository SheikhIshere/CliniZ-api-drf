from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient

# Create your models here.

class Specialization(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Designation(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name

class AvailableTime(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor/images')
    designation = models.ManyToManyField(Designation)
    Specialization = models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    fee = models.IntegerField()
    meet_link = models.CharField(max_length=100)
    
    def __str__(self):
        first = (self.user.first_name or "").strip()
        last = (self.user.last_name or "").strip()
        name = f"{first} {last}".strip()
        return self.user.username or f"{name}"

    

START_CHOICE = [
    ('٭', '٭'),
    ('٭٭', '٭٭'),
    ('٭٭٭', '٭٭٭'),
    ('٭٭٭٭', '٭٭٭٭'),
    ('٭٭٭٭٭', '٭٭٭٭٭'),
]

class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    star = models.CharField(max_length=5, choices=START_CHOICE)

    def __str__(self):
        return f"{self.reviewer.user.username} reviewd {self.doctor.user.username} with {self.star} stars"