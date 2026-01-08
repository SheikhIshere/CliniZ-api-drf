"""
doctors/models.py
"""

# core imports
from django.db import models

# base model import
from BASE.base_model import (
    BaseModel,
    BaseProfile,    
    DoctorAttribute,
)
from BASE.base_choice import (
    DoctorVerificationStatus,
    DoctorPersonalStatus,
    StarRating,
)

# patient
from patients.models import Patient



"""
doctor designation
"""
class Designation(DoctorAttribute):
    pass


"""
doctor's specialization
"""
class Specialization(DoctorAttribute):
    pass


"""
doctor's available time
"""
class AvailableTime(DoctorAttribute):
    pass


"""
doctor model
"""
class Doctor(BaseProfile):
    # info
    photo = models.ImageField(upload_to='doctors/profile_pictures/', blank=True, null=True)
    
    # doctor type
    designation = models.ManyToManyField(Designation, blank=True)
    specialization = models.ManyToManyField(Specialization, blank=True)
    available_time = models.ManyToManyField(AvailableTime, blank=True)

    # doctor business
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    year_of_experience = models.PositiveIntegerField(default=0)

    # admin investigation
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20, 
        choices=DoctorVerificationStatus.choices,
        help_text="Verification status of the doctor, maintained by admin",
        blank=True,
        null=True
    )
    
    # doctor choice
    personal_status = models.CharField(
        max_length=20, 
        choices=DoctorPersonalStatus.choices, 
        default=DoctorPersonalStatus.ACTIVE,
        help_text="Personal status of the doctor",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Dr. {self.full_name or self.user.email}"
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


"""
doctor's qualification
"""
class Qualification(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    year = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    registration_id = models.CharField(max_length=100, blank=True, unique=True)
    certificate_img = models.ImageField(upload_to='doctors/qualifications/', blank=True, null=True)

    # for admin
    verification_status = models.CharField(
        max_length=20, 
        choices=DoctorVerificationStatus.choices,
        help_text="Verification status of the qualification, maintained by admin",
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.title} - {self.degree} from {self.institution} ({self.year})"


    class Meta:
        verbose_name = "Doctor Qualification"
        verbose_name_plural = "Doctor Qualifications"



"""
review section for doctors
"""
class Review(BaseModel):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.CharField(max_length=500, blank=True)
    star = models.IntegerField(choices=StarRating.choices)
    
    def __str__(self):
        return f"{self.reviewer.user.full_name or self.reviewer.user.email} reviewed dr.{self.doctor.user.full_name or self.doctor.user.email} with {self.star} stars"






