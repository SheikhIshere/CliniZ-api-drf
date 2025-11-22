from rest_framework import serializers
from .models import (
    Doctor, 
    AvailableTime, 
    Designation, 
    Specialization,
    Review
)


class DoctorSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many = False)
    # designation = serializers.HyperlinkedRelatedField(
        # many = True, 
        # view_name = 'designation-detail', 
        # read_only = True
    # )
    # Specialization = serializers.StringRelatedField(many = True)
    # available_time = serializers.StringRelatedField(many = False)

    class Meta:
        model = Doctor
        fields = '__all__'

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

