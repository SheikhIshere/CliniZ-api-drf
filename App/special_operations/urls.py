"""
special_operations/urls.py
"""
from django.urls import path
from .views import DoctorRegistrationCreateView, DoctorRegistrationApplicationView, DoctorRegistrationApplicationDetailsView


urlpatterns = [
    path('apply/to-be/doctor/', DoctorRegistrationCreateView.as_view(), name='apply-to-be-doctor'),
    path('apply/to-be/doctor/list', DoctorRegistrationApplicationView.as_view(), name='apply-to-be-doctor-list'),
    path('apply/to-be/doctor/detail/<int:pk>/', DoctorRegistrationApplicationDetailsView.as_view(), name='apply-to-be-doctor-detail'),
]