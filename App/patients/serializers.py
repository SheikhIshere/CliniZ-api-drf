"""
Patient serializers
"""
import email
from rest_framework import serializers
from .models import Patient

"""
to see the list of patient
"""
class PatientListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()

    def get_email(self, obj) -> str | None:
        return obj.user.email if obj.user else None
    
    def get_account_type(self, obj) -> str | None:
        return obj.user.role

    class Meta:
        model = Patient
        fields = [
            'id', 
            'email',
            'full_name', 
            'photo',
            'gender', 
            'age', 
            'blood_group',
            'account_type',
            'created_at',
        ]
        read_only_fields = [
            'created_at', 
            'updated_at', 
            'email', 
            'account_type',
        ]


"""
retrieve single patient profile 
for own use and other users
"""
class PatientDetailSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()

    def get_email(self, obj) -> str | None:
        return obj.user.email if obj.user else None
    
    def get_account_type(self, obj) -> str | None:
        return obj.user.role if obj.user else None
        
    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'email',
            'full_name',
            'photo',
            'birthday',
            'gender',
            'age',
            'blood_group',
            'height',
            'weight',
            'phone_number',
            'address',
            'token',
            'account_type',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'created_at', 
            'updated_at', 
            'user', 
            'email',
            'token',
            'account_type',
        ]

