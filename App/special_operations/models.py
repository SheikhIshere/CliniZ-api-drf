"""
special_operations
"""
# core imports
from django.db import models
from BASE.base_model import BaseModel
from BASE.base_choice import MigrateProfileStatus


# local model
from doctors.models import Doctor, Qualification
from patients.models import Patient

class DoctorRegistration(BaseModel):
    """Model to store doctor registration requests"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    registration_number = models.CharField(max_length=100, unique=True)
    certificate_img = models.ImageField(upload_to='doctor_certificates/')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    certificate_registration_number = models.CharField(max_length=100)
    year = models.DateField()

    activation_status = models.CharField(
        max_length=20,
        choices=MigrateProfileStatus.choices,
        default=MigrateProfileStatus.PENDING
    )

    class Meta:
        db_table = 'doctor_registration'
        verbose_name = 'Profile Migration Application'
        verbose_name_plural = 'Profile Migrations Applications'

    def __str__(self):
        return f"Doctor Registration - {self.registration_number}"

    def __str__(self):
        return f"Doctor Registration - {self.registration_number}"

    def save(self, *args, **kwargs):
        # Run migration logic BEFORE saving, but DO NOT delete patient yet
        if self.activation_status == MigrateProfileStatus.ACCEPTED and self.patient_id:
            # Prevent running migration multiple times
            if Doctor.objects.filter(user=self.patient.user).exists():
                return super().save(*args, **kwargs)

            user = self.patient.user

            full_name = self.patient.full_name
            photo = getattr(self.patient, 'photo', None)
            birthday = self.patient.birthday
            gender = self.patient.gender
            age = self.patient.age
            blood_group = self.patient.blood_group
            height = self.patient.height
            weight = self.patient.weight
            phone_number = self.patient.phone_number
            address = self.patient.address
            token = self.patient.token
            registration_number = self.registration_number

            # Update user role
            user.role = 'doctor'
            user.save()

            # Create Doctor profile
            doctor = Doctor.objects.create(
                user=user,
                full_name=full_name,
                photo=photo,
                birthday=birthday,
                gender=gender,
                age=age,
                blood_group=blood_group,
                height=height,
                weight=weight,
                phone_number=phone_number,
                address=address,
                token=token,
                registration_number=registration_number,
                is_verified=True
            )

            # Create Qualification for the doctor
            Qualification.objects.create(
                doctor=doctor,
                title=self.degree,
                institution=self.institution,
                degree=self.degree,
                year=self.year,
                registration_id=self.certificate_registration_number,
                certificate_img=self.certificate_img,
                verification_status='verified'
            )

        # TODO: implement celery and make a schedule, after this migrations done the patient account will be deleted in next 24 hour ok
        
        # Save DoctorRegistration row first
        super().save(*args, **kwargs)

