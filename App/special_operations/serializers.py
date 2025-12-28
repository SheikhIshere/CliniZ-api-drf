# core imports 
from rest_framework import serializers
from django.contrib.auth import get_user_model

# local imports
from .models import DoctorRegistration
from patients.models import Patient  # Import Patient model

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
        
        # Check if registration number already exists
        if DoctorRegistration.objects.filter(registration_number=registration_number).exists():
            raise serializers.ValidationError("A registration request with this number already exists.")
        
        # Now filter with Patient instance instead of User
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status__in=['PENDING']).exists():
            raise serializers.ValidationError("You have already submitted a registration request with this number.")

        # check if rejected or not
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status__in=['REJECTED']).exists():
            raise serializers.ValidationError("You have already submitted a registration request with this number that was rejected. Please contact support if you believe this is an error.")
        
        # check if he already have this certificate or not
        if DoctorRegistration.objects.filter(patient=patient, registration_number=registration_number, activation_status__in=['APPROVED']).exists():
            raise serializers.ValidationError("You have already been approved as a doctor with this registration number.")
        
        return attrs

    def create(self, validated_data):
    

        user = self.context.get('request').user
        
        # Get the Patient instance associated with the user
        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient profile not found for this user.")
        
        return DoctorRegistration.objects.create(patient=patient, **validated_data)

