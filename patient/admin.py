from django.contrib import admin
from .models import Patient
# Register your models here.


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user', 'mobile_no']
    search_fields = ['user', 'mobile_no']
    list_filter = ['user', 'mobile_no']

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name