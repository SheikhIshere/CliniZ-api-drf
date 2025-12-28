"""
doctors/serializers.py
"""

from rest_framework import serializers
from .models import (
    Designation, 
    Specialization,
    AvailableTime,
    Doctor, 
    Qualification, 
    Review,
)

"""
doctor serialization where we are passing see through fields
"""
class DoctorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role  = serializers.CharField(source="user.role", read_only=True)
    
    class Meta:
        model = Doctor
        exclude = (
            'user',
        )
        read_only_fields = (
            'email', 
            'role', 
            'is_verified', 
            'registration_number',
            'verification_status', 
            'token',
        )


"""
this is a designation serializer for patient view
"""
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        exclude = (
            'slug',
        )        
        read_only_fields = (
            'created_at',
            'updated_at',
        )

"""
this is a specialization serializer for patient view
"""
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        exclude = (
            'slug',
        )



"""
doctor's available time , on what time patient can book his/her meeting
"""
class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        exclude = (
            'slug',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
        )


"""

This is a review serializer for patient view
"""
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('doctor',)
        read_only_fields = ('created_at',)


"""
if doctor try to apply to add an qualification
"""
class QualificationApplySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="doctor.user.email", read_only=True)

    class Meta:
        model = Qualification
        exclude = ('doctor',)
        read_only_fields = ('verification_status','created_at','updated_at','email')

    def validate(self, attrs):
        applier = self.context['request'].user.doctor
        registration_id = attrs.get('registration_id')
        title = attrs.get('title')
        institution = attrs.get('institution')
        degree = attrs.get('degree')
        year = attrs.get('year')
        grade = attrs.get('grade')

        if registration_id:
            existing = Qualification.objects.filter(
                doctor=applier,
                registration_id=registration_id
            ).first()

            if existing:
                if existing.verification_status == 'APPROVED':
                    raise serializers.ValidationError({"error": "Already approved."})
                if existing.verification_status == 'PENDING':
                    raise serializers.ValidationError({"error": "Under review."})

        existing = Qualification.objects.filter(
            doctor=applier,
            title=title,
            institution=institution,
            degree=degree,
            year=year,
            grade=grade,
        ).first()

        if existing and existing.verification_status != 'APPROVED':
            raise serializers.ValidationError({"error": "Pending approval."})

        return attrs

    def create(self, validated_data):
        doctor = self.context['request'].user.doctor
        qualification = Qualification.objects.create(
            doctor=doctor,
            verification_status='PENDING',
            **validated_data
        )


        # here i am sending mail to user that his application has been submitted
        # TODO: Implement email sending logic here
        # For now, just return the created qualification

        return qualification


"""
this serializer is for viewing doctor's qualifications
to all verified users
"""
class DoctorQualificationsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='doctor.user.email', read_only=True)
    class Meta:
        model = Qualification
        fields = '__all__'
        read_only_fields = (
            'doctor', 
            'email',
            'verification_status', 
            'created_at', 'updated_at',
        )










