"""
appointments/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientAppointmentViewSet, DoctorAppointmentViewSet

router = DefaultRouter()
router.register(r'patient', PatientAppointmentViewSet, basename='patient-appointments')
router.register(r'doctor', DoctorAppointmentViewSet, basename='doctor-appointments')

urlpatterns = [
    path('', include(router.urls)),
]
