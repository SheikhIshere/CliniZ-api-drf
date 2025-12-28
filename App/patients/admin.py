"""
patients/admin.py
Admin configuration for patient models.
"""
# core import
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'full_name', 'gender', 'age', 'blood_group', 'token', 'user__role', 'created_at']
    search_fields = ['user_role', 'user__email', 'user__full_name']
    list_filter = ['gender', 'created_at', 'token', 'blood_group']
    ordering = ['-created_at', 'token', 'height', 'weight']

    def email(self, obj):
        return obj.user.email if obj.user else '-'
