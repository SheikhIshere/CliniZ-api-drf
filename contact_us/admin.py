from django.contrib import admin
from .models import ContactUs
# Register your models here.


# admin.site.register(ContactUs)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'problem')
    search_fields = ('name', 'phone')
    list_filter = ('name', 'phone')

