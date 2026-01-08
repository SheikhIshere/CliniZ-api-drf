"""
special_operations/views.py
"""

from rest_framework import generics
from .models import DoctorRegistration
from .serializers import BecomeDoctorSerializer, BecomeDoctorApplicationSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

@extend_schema(tags=['profile migration'])
class DoctorRegistrationCreateView(generics.CreateAPIView):
    queryset = DoctorRegistration.objects.all()
    serializer_class = BecomeDoctorSerializer
    permission_classes = (IsAuthenticated,)


    
@extend_schema(tags=['profile migration'])
class DoctorRegistrationApplicationView(generics.ListAPIView):
    serializer_class = BecomeDoctorApplicationSerializer
    queryset = DoctorRegistration.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return DoctorRegistration.objects.filter(patient__user=user)

@extend_schema(tags=['profile migration'])
class DoctorRegistrationApplicationDetailsView(generics.RetrieveAPIView):
    serializer_class = BecomeDoctorApplicationSerializer
    queryset = DoctorRegistration.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        # TODO: this can be updated using select_related
        return DoctorRegistration.objects.filter(patient__user=user)
    