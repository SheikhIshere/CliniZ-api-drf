"""
appointments/admin.py
"""
from django.contrib import admin
from .models import Appointments, AppointmentImage

class AppointmentImageInline(admin.TabularInline):
    model = AppointmentImage
    extra = 1
    fields = ('image',)

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = (
        'doctor', 'patient', 'appointment_type', 
        'title', 'status', 'meeting_date', 'meeting_time', 'is_paid'
    )
    list_filter = ('status', 'appointment_type', 'meeting_date')
    search_fields = ('doctor__user__full_name', 'patient__user__full_name', 'title', 'symptoms')
    inlines = [AppointmentImageInline]

@admin.register(AppointmentImage)
class AppointmentImageAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'image')
    search_fields = ('appointment__doctor__user__full_name', 'appointment__patient__user__full_name')
