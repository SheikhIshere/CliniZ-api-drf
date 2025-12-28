"""
AdminPortal/admin.py
"""

# core imports
from django.contrib import admin

# local imports
from .models import ContactUs, ReportBug, Service

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):    
    list_display = ['user__email', 'email', 'problem', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'email', 'problem']

@admin.register(ReportBug)
class ReportBugAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'bug_type', 'status', 'created_at']
    list_filter = ['bug_type', 'status', 'created_at']
    search_fields = ['user__email', 'email', 'bug_other']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']