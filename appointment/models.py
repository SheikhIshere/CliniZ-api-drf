from django.db import models
from patient.models import Patient
from doctor.models import Doctor, AvailableTime
# Create your models here.


APPOINMENT_STATUS = (
    ("Complead", "Complead"),
    ("Pending", "Pending"),
    ("Running", "Running")
)

APPOINMENT_TYPE = (
    ('Online', 'Online'),
    ('Offline', 'Offline')
)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appoinment_types = models.CharField(max_length=30, choices=APPOINMENT_TYPE)
    appoinment_status = models.CharField(max_length=30, choices=APPOINMENT_STATUS, default='Pending')
    symtom = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.user.username} appoinment with DR. {self.doctor.user.username} at {self.time}"