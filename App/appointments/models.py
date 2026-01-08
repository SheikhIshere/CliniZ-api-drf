"""
appointments/models.py
"""

# base import
from BASE.base_model import BaseModel
from django.db import models

# choice 
from BASE.base_choice import AppointmentStatus, AppointmentType

# doctor
from doctors.models import Doctor, AvailableTime
# patient
from patients.models import Patient


"""
this is for doctor & patient
to set an appointment together
"""
class Appointments(BaseModel):
    # the main relation ship
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    # added by patient
    appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices)
    title = models.CharField(
        max_length=100, 
        help_text="3-4 word summary of your issue",
    ) # in future this will be auto summarized by ai
    symptoms = models.TextField(help_text="Describe the symptoms or reason for consultation")

    # for doctor
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    
    # time of meeting
    meeting_date = models.DateField(help_text="Meeting date")
    meeting_time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    meeting_link = models.CharField(max_length=200, blank=True, null=True)

    # payment
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
    
    def __str__(self):
        return f"Dr. {self.doctor.full_name} ↔ patient: {self.patient.full_name} @ {self.meeting_time} - status: {self.status}"



"""
This will help patient upload multiple symptom images for an appointment.
eg: he got rash in many places fixed number of image might couldn't work well, 
    so we allow multiple images. This provides flexibility for 
    patients to share as many relevant images as needed.
"""
class AppointmentImage(BaseModel):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="appointment/patient/symptom_img/")
    
    