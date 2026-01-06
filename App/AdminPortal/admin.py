"""
AdminPortal/admin.py
"""

# core imports
from django.contrib import admin

# local imports
from .models import ContactUs, ReportBug, Service

admin.site.register(ContactUs)
admin.site.register(ReportBug)
admin.site.register(Service)
