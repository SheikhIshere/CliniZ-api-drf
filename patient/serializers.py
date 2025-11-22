from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Patient
from bad_word_list.bad_words import bad_words # this is list of bad words


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many = False)
    class Meta:
        model = Patient
        fields = '__all__'

class RegistrationsSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password'
        ]

    def validate_username(self, value):
        """Validate username for bad words"""
        username_lower = value.lower()
        
        # Check if username contains any bad words
        for bad_word in bad_words:
            if bad_word in username_lower:
                raise serializers.ValidationError('Username contains inappropriate content')
        
        return value

    def validate_first_name(self, value):
        """Validate first name for bad words"""
        if value:  # Only validate if first_name is provided
            first_name_lower = value.lower()
            
            # Check if first name contains any bad words
            for bad_word in bad_words:
                if bad_word in first_name_lower:
                    raise serializers.ValidationError('First name contains inappropriate content')
        
        return value

    def validate_last_name(self, value):
        """Validate last name for bad words"""
        if value:  # Only validate if last_name is provided
            last_name_lower = value.lower()
            
            # Check if last name contains any bad words
            for bad_word in bad_words:
                if bad_word in last_name_lower:
                    raise serializers.ValidationError('Last name contains inappropriate content')
        
        return value

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username_error': 'Username already exists'})
            else:
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError({'email_error': 'Email already exists'})
                else:            
                    user = User(username=username, first_name=first_name, last_name=last_name, email=email)
                    user.set_password(password)  
                    user.is_active = False
                    user.save()             
                    return user
        else:
            raise serializers.ValidationError({'password_error': 'Password does not match'})
        

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)