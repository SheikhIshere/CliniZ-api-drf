"""
appointments/views.py
"""
# core imports
from rest_framework import (
    generics,
    viewsets,
    status,
    mixins
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# model import
from .models import Appointments
from doctors.models import Doctor

# serializers
from .serializers import (
    PatientAppointmentSerializer,
    DoctorAppointmentListSerializer,
    AppointmentPatientDetailSerializer,
    DoctorAppointmentUpdateStatusSerializer,
)

# sending mail
from django.core.mail import send_mail
from django.conf import settings

# custom permission
from BASE.base_permissions import IsDoctor, IsVerifiedUser, IsPatient

# api documentation
from drf_spectacular.utils import extend_schema

"""
This is for patient appointments.
Patients can view, create, read, and update their own appointments.
"""
@extend_schema(
    tags=['Appointment'],
    description=
    """
    patients can create an appointment, see and retrieve their own appointments
    """,
)
class PatientAppointmentViewSet(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    queryset = Appointments.objects.all()
    serializer_class = PatientAppointmentSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser, IsPatient]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        doctor_id = self.request.data.get('doctor')
        if doctor_id:
            context['doctor'] = Doctor.objects.get(id=doctor_id)
        return context

    def get_queryset(self):
        # patient sees only their own appointments
        return self.queryset.filter(patient=self.request.user.patient)





"""
doctor sees appointment list and details
"""
@extend_schema(
    tags=['Appointment'],
    description=
    """
    A doctor can see the appointments they have,
    view patient details, and update appointment status.
    """,
)
class DoctorAppointmentViewSet( mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet,
):
    queryset = Appointments.objects.all()
    permission_classes = [IsAuthenticated, IsDoctor, IsVerifiedUser]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AppointmentPatientDetailSerializer
        elif self.action == 'update_status':
            return DoctorAppointmentUpdateStatusSerializer
        return DoctorAppointmentListSerializer

    def get_queryset(self):
        # doctor sees only their own appointments
        return self.queryset.filter(doctor=self.request.user.doctor).order_by('created_at')

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        
        if serializer.is_valid():
            previous_status = appointment.status
            new_status = serializer.validated_data.get('status', previous_status)

            # enforce running → completed flow
            if previous_status == 'PENDING' and new_status == 'COMPLETED':
                return Response(
                    {"detail": "Appointment must be running before it can be completed."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()  # update status and meeting link

            # send email to patient
            patient_email = appointment.patient.user.email
            doctor_name = appointment.doctor.full_name
            subject = f"Update on your appointment with Dr. {doctor_name}"
            message = f"Your appointment status is now: {new_status}."
            
            if appointment.meeting_link:                
                message += f" Join using this link: {appointment.meeting_link} \n Please be ready on {appointment.meeting_date} at {appointment.meeting_time}."
            
            
            print(f"DEBUG: Sending email to {patient_email} with subject '{subject}'")
            print(f"DEBUG: Message: {message}")

            #TODO: in future this will be handled by celery and message broker
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient_email],
                fail_silently=True
            )

            return Response({"detail": "Appointment status updated and patient notified."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





