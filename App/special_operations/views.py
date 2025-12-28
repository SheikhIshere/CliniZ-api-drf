"""
special_operations/views.py
"""

from rest_framework import generics
from .models import DoctorRegistration
from .serializers import BecomeDoctorSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['profile migration'])
class DoctorRegistrationCreateView(generics.CreateAPIView):
    queryset = DoctorRegistration.objects.all()
    serializer_class = BecomeDoctorSerializer
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
    