"""
patients/urls.py
"""
# core imports
from django.urls import path

# local import
from .views import(
    PatientListView,
    PatientDetailView,
    PatientMeView,
)

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/me/', PatientMeView.as_view(), name='patient-me'),
    path('patients/<str:user__email>/', PatientDetailView.as_view(), name='patient-detail'),
]