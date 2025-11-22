from django.contrib import admin
from .models import (
    Doctor, AvailableTime, 
    Designation, Specialization,
    Review
)

admin.site.register(Doctor)
admin.site.register(AvailableTime)
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Review)