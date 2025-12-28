"""
special_operations/urls.py
"""
from django.urls import path
from .views import DoctorRegistrationCreateView


urlpatterns = [
    path('apply/to-be/doctor/', DoctorRegistrationCreateView.as_view(), name='apply-to-be-doctor'),
]