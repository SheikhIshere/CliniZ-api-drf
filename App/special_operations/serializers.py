# core imports 
from rest_framework import serializers
from django.contrib.auth import get_user_model

# local imports
from .models import DoctorRegistration
from patients.models import Patient  # Import Patient model

# base import
from BASE.base_choice import MigrateProfileStatus

# Qualification
from doctors.models import Qualification

User = get_user_model()

class BecomeDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegistration
        exclude = ['id','patient','activation_status', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context.get('request').user
        
        # Get the Patient instance associated with the user
        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient profile not found for this user.")
        
        registration_number = attrs.get('registration_number')
        
        # checking if the user is already doctor or not
        if user.role == 'doctor':
            raise serializers.ValidationError({"warning": "You are already registered as a doctor."})

        # Now filter with Patient instance instead of User
        if Qualification.objects.filter(registration_id=attrs.get('certificate_registration_number')).exists():
            raise serializers.ValidationError({"warning": "Please add your own certificate. else contact authority"})

        # Now filter with Patient instance instead of User
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status=MigrateProfileStatus.PENDING).exists():
            raise serializers.ValidationError({"warning": "You have already submitted a request with Your Doctor registration number. we are processing it. we will let you know the result soon."})

        # check if he already have this certificate or not
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status=MigrateProfileStatus.ACCEPTED).exists():
            raise serializers.ValidationError("You have already been approved as a doctor with this registration number.")        

        # check if rejected or not
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status=MigrateProfileStatus.REJECTED).exists():
            raise serializers.ValidationError("You have already submitted a registration request with this number that was rejected. Please contact support if you believe this is an error.")
        
        # Check if registration number already exists
        if DoctorRegistration.objects.filter(registration_number=registration_number).exists():
            raise serializers.ValidationError({"warning": "A registration request with this number already exists."})

        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        
        # Get the Patient instance associated with the user
        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient profile not found for this user.")
        
        return DoctorRegistration.objects.create(patient=patient, **validated_data)



"""
application get all and retrieve
"""
class BecomeDoctorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegistration
        fields = (
            'id',
            'registration_number', 
            'certificate_img',
            'institution',
            'degree',
            'year',         
            'activation_status',         
            )
