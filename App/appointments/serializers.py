"""
appointments/serializers.py
"""
# core import
from contextlib import nullcontext
from rest_framework import serializers

import patients

# model import
from .models import (
    Appointments, 
    AppointmentImage
)


"""
patient will be able to add picture while creating appointment
"""
class AppointmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentImage
        fields = ('image',)


"""
for patient
patient will be creating a appointment with doctor
"""
class PatientAppointmentSerializer(serializers.ModelSerializer):
    images = AppointmentImageSerializer(many=True, required=False)

    class Meta:
        model = Appointments
        exclude = ('status', 'meeting_link',)
        read_only_fields = ('doctor', 'patient', 'created_at', 'updated_at')

    def validate(self, attrs):
        doctor = self.context.get('doctor')
        meeting_date = attrs.get('meeting_date')
        meeting_time = attrs.get('meeting_time')
        appointment_type = attrs.get('appointment_type')

        if Appointments.objects.filter(
            doctor=doctor,
            meeting_date=meeting_date,
            meeting_time=meeting_time,
            appointment_type=appointment_type,
            status='PENDING'
        ).exists():
            raise serializers.ValidationError({
                "details": "Doctor is already booked for this time slot."
            })

        # checking is token of patient sufficient
        patient = self.context['request'].user.patient
        if patient.token < doctor.fee: 
            raise serializers.ValidationError({
                "details": (
                    f"Booking failed due to insufficient tokens. "
                    f"Appointment with Dr. {doctor.user.get_full_name()} requires {doctor.fee} tokens, "
                    f"but your balance is {patient.token} tokens. "
                    "Please purchase additional tokens to proceed."
                )
            })

        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        doctor = self.context['doctor']
        patient = self.context['request'].user.patient


        # cutting token from patient
        patient.token -= doctor.fee 

        # adding token into doctor's account
        doctor.token += doctor.fee
        doctor.save()

        # creating appointment
        appointment = Appointments.objects.create(
            doctor=doctor,
            patient=patient,
            is_paid=True,
            status='pending'
            **validated_data
        )
        
        for img in images_data:
            AppointmentImage.objects.create(appointment=appointment, **img)

        return appointment


"""
for doctor
from doctor aspect seeing his dashboard what type of meetings he got
with patients - this serializer will show all appointments for a doctor
"""
class DoctorAppointmentListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    patient_photo = serializers.ImageField(source='patient.photo', read_only=True)

    class Meta:
        model = Appointments
        fields = ('patient_photo', 'patient_name', 'meeting_date', 'meeting_time', 'appointment_type', 'status', 'is_paid')



"""
for doctor
showing details of patient to Doctor Appointment Section or model
this serializer will show detailed information about a specific patient's 
appointment, like name age address etc
"""
class AppointmentPatientDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='patient.full_name', read_only=True)
    age = serializers.CharField(source='patient.age', read_only=True)    
    address = serializers.CharField(source='patient.address', read_only=True)
    email = serializers.CharField(source='patient.user.email', read_only=True)
    patient_photo = serializers.ImageField(source='patient.photo', read_only=True)
    height = serializers.CharField(source='patient.height', read_only=True)
    weight = serializers.CharField(source='patient.weight', read_only=True)
    phone_number = serializers.CharField(source='patient.phone_number', read_only=True)
    blood_group = serializers.CharField(source='patient.blood_group', read_only=True)
    gender = serializers.CharField(source='patient.gender', read_only=True)

    symptom_images = serializers.SerializerMethodField()

    def get_symptom_images(self, obj):
        images = obj.images.all()
        return AppointmentImageSerializer(images, many=True).data

    class Meta:
        model = Appointments
        fields = (
            'name', 
            'age', 
            'address', 
            'email', 
            'patient_photo', 
            'height', 
            'weight', 
            'phone_number', 
            'blood_group',
            'gender',
            'symptoms', 
            'title',
            'meeting_date',
            'meeting_time',
            'is_paid',
            'symptom_images',
            'created_at'
        )
    

"""
doctor can make any appointment running
"""
class DoctorAppointmentUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ('status', 'meeting_link',)

    def validate_status(self, value):
        current_status = self.instance.status

        allowed_transitions = {
            'PENDING': ['RUNNING'],
            'RUNNING': ['COMPLETED'],
            'COMPLETED': [],  # once completed, no further changes
        }

        if current_status not in allowed_transitions:
            raise serializers.ValidationError("Invalid current status.")

        if value not in allowed_transitions[current_status]:
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}."
            )
        return value
        


"""
will add a payment fraud system for patient if doctor takes payment and
marks appointment as completed. This will help track suspicious 
activities and prevent fraudulent payments. The system will monitor 
for patterns like multiple quick payments, mismatched appointment 
details, or unusual payment amounts. It will flag suspicious transactions
for manual review and maintain an audit trail of all flagged activities.
This system will help ensure payment integrity and protect both patients 
and doctors from fraudulent activities by providing transparency and 
accountability in all transactions.
"""




