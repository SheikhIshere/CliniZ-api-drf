"""
special_operations/admin.py
"""

# core import 
from django.contrib import admin

# local import
from .models import DoctorRegistration

@admin.register(DoctorRegistration)
class DoctorRegistrationAdmin(admin.ModelAdmin):
    list_display = ['patient__user__email', 'registration_number','institution','degree','year', 'activation_status']
    list_filter = ['activation_status', 'year']
    date_hierarchy = 'created_at'
    search_fields = ['patient__user__email', 'registration_number']
    ordering = ['-created_at']