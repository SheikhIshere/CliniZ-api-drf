"""
patients/views.py
"""
# core imports
from rest_framework import(
    status,
    permissions,
    generics,
)
from rest_framework.response import Response

from patients.models import Patient

# local imports
from .serializers import(
    PatientListSerializer,
    PatientDetailSerializer,
)
from .models import (
    Patient
)

# custom permission
from BASE.base_permissions import IsVerifiedUser, IsOwnerOrReadOnly

# schema design
from drf_spectacular.utils import extend_schema


"""
showing list of profile in order to check permissions and data
"""
@extend_schema(
    tags=['Patients'],
    description="List all patient profiles with filtering options.",
)
class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    
    def get_queryset(self):
        return Patient.objects.all()


"""
retrieve profile for others
"""
@extend_schema(
    tags=['Patients'],
    description="Retrieve a patient profile by email."
)
class PatientDetailView(generics.RetrieveAPIView):
    queryset = Patient.objects.select_related("user")
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsOwnerOrReadOnly, ]
    serializer_class = PatientDetailSerializer
    lookup_field = 'user__email'


"""
Retrieve, update, or delete own patient profile.
"""
@extend_schema(
    tags=['Patients'],
    description="Retrieve, update, or delete your own patient profile."
)
class PatientMeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsOwnerOrReadOnly]

    def get_object(self):
        patient_profile, _ = Patient.objects.select_related('user').get_or_create(user=self.request.user)
        return patient_profile
    
    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        user = patient.user
        
        self.perform_destroy(patient)
        user.delete()
        return Response({
            'deleted': 'patient profile deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)