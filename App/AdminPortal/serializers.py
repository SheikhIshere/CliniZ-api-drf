"""
AdminPortal/serializers.py
"""
# core import
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# local import
from .models import(
    ContactUs,
    Service,
    ReportBug
)

from doctors.models import Review


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        extra_kwargs = {
            'problem': {'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            validated_data['user'] = user
            validated_data['email'] = user.email
        # else: guest will manually pass email

        return super().create(validated_data)


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ReportBugSerializer(ModelSerializer):
    class Meta:
        model = ReportBug
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        
        if user and user.is_authenticated:
            validated_data['user'] = user
            validated_data['email'] = user.email
        # else: guest will manually pass email

        return super().create(validated_data)


class ReviewSerializerPublic(ModelSerializer):
    name = serializers.CharField(source='reviewer.full_name', read_only=True)
    image = serializers.ImageField(source='reviewer.photo', read_only=True)
    class Meta:
        model = Review
        fields = ['name', 'image', 'star', 'body', 'created_at']
        read_only_fields = ('name', 'image', 'star', 'body', 'created_at')