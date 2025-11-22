# from django.contrib import admin
# from .models import Appointment

# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('patient_name', 'doctor_name', 'appoinment_types', 'appoinment_status', 'time', 'cancel')
#     search_fields = ('patient_name', 'doctor_name', 'appoinment_types', 'appoinment_status', 'time', 'cancel')
#     list_filter = ('patient_name', 'doctor_name', 'appoinment_types', 'appoinment_status', 'time', 'cancel')

#     def doctor_name(self, obj):
#         return obj.Doctor.user.get_full_name() or obj.Doctor.user.username

#     def patient_name(self, obj):
#         return obj.Patient.user.get_full_name() or obj.Patient.user.username
    

from django.contrib import admin
from .models import Appointment
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor_name', 'appoinment_types', 'appoinment_status', 'time', 'cancel')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name', 'appoinment_types', 'appoinment_status')
    list_filter = ('patient', 'doctor', 'appoinment_types', 'appoinment_status', 'time', 'cancel')

    def doctor_name(self, obj):
        return obj.doctor.user.get_full_name() or obj.doctor.user.username

    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    
    def save_model(self, request, obj, form, change):
        obj.save()
        # check list debugging
        # print(f"appointment status: {obj.appoinment_status}")
        # print(f'appoinment_types: {obj.appoinment_types}')

        print('before if condition at admin.py')        
        if obj.appoinment_status == 'Running' and obj.appoinment_types == 'Online':
            
            # arived
            print('arived into if condition')
            
            email_subject = f"Your appoinment is {obj.appoinment_status} "
            email_body = render_to_string(
                "mail/admin_email.html",
                {                    
                    'patient_name': obj.patient.user.get_full_name() or obj.patient.user.username,
                    'doctor_name': obj.doctor.user.get_full_name() or obj.doctor.user.username,
                    'meet_link': obj.doctor.meet_link,
                    'appoinment_types': obj.appoinment_types,
                    'appoinment_status': obj.appoinment_status,
                    
                },
            )

            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[obj.patient.user.email],
            )
            email.attach_alternative(email_body, 'text/html')

            # debugging only
            # print(f"appointment status: {obj.appoinment_status}")
            # print(f'appoinment_types: {obj.appoinment_types}')
            # print(f'doctor name: {obj.doctor.user.get_full_name() or obj.doctor.user.username}')
            # print(f'patient name: {obj.patient.user.get_full_name() or obj.patient.user.username}')
            # print(f"to: {obj.patient.user.email}")
            # print(f"email_subject: {email_subject}")
            # print(f"email_body: {email_body}")
            # print(f"email: {email}")
            # print(f'meet_link: {obj.doctor.meet_link}')            

            email.send()

            # print("\nEmail sent successfully.")
            