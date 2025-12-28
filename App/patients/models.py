"""
patients/models.py
"""
# core imports
from django.db import models
from BASE.base_model import BaseProfile


"""
patient profile
"""
class Patient(BaseProfile):
    photo = models.ImageField(upload_to='patients/profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.full_name or self.user.email}"
