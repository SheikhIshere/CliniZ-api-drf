"""
doctor/admin.py
"""
from django.contrib import admin
from .models import Doctor, Qualification, Designation, Specialization, AvailableTime, Review

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user__email","full_name", "fee", "year_of_experience", "is_verified", "verification_status", "personal_status")
    list_filter = ("is_verified", "verification_status", "personal_status")
    search_fields = ("full_name", "user__email", "registration_number")

    
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("doctor", "degree", "institution", "year", "verification_status", "registration_id")
    list_filter = ("verification_status", "institution")
    search_fields = ("degree", "institution", "registration_id", "doctor__user__email")

    
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)

    
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

    
@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "doctor", "star", "created_at")
    list_filter = ("star", "created_at")
    search_fields = ("reviewer__user__email", "doctor__user__email", "body")

    