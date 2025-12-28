"""
doctors/views.py
"""
# core imports
from rest_framework import (
    generics,
    permissions,
    viewsets,
    filters,
    status,
)
from rest_framework.response import Response
from rest_framework.views import APIView

# from BASE permissions
from BASE.base_permissions import (
    IsVerifiedUser, 
    IsOwnerOrReadOnly,
    IsNotReviewingSelf,
    IsDoctor,
)
from BASE.base_pagination import BasePagination
from BASE.base_views import BaseDoctorViewSet

# models
from .models import (
    Designation,
    Specialization,
    AvailableTime,
    Doctor,
    Qualification,
    Review
)

# serializers
from .serializers import (
    DoctorSerializer,
    DesignationSerializer,
    SpecializationSerializer,
    AvailableTimeSerializer,
    QualificationApplySerializer,
    ReviewSerializer,
    DoctorQualificationsSerializer
)

# api documentation
from drf_spectacular.utils import extend_schema


"""
doctor's list
"""
@extend_schema(tags=["Doctors"])
class DoctorListView(generics.ListAPIView, BasePagination):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return super().get_queryset()


"""
patient can see doctor's profile
"""
@extend_schema(tags=["Doctors"])
class DoctorsProfile(generics.RetrieveAPIView):
    queryset = Doctor.objects.select_related("user")
    serializer_class = DoctorSerializer
    lookup_field = 'user__email'


"""
retrieve update and delete own profile
"""
@extend_schema(tags=["Doctors"])
class DoctorMeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsOwnerOrReadOnly, IsDoctor]

    def get_object(self):
        doctor_profile, _ = Doctor.objects.select_related('user').get_or_create(user=self.request.user)
        return doctor_profile
    
    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        user = doctor.user
        
        self.perform_destroy(doctor)
        user.delete()
        return Response({
            'deleted': 'doctor profile deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


"""
doctor's available time
"""
@extend_schema(tags=["Available Time OF Doctor"])
class AvailableTimeViewSet(BaseDoctorViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer


"""
doctor's available time to patient
"""
class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(doctor=doctor_id)
        return queryset


"""
available time for specific doctor
"""
@extend_schema(tags=["Available Time OF Doctor"])
class AvailableTimeForPatientViewSet(BaseDoctorViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer    
    filter_backends = [AvailableTimeForSpecificDoctor]


"""
doctor's designation
"""
@extend_schema(tags=["Designation OF Doctor"])
class DesignationViewSet(BaseDoctorViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


"""
doctor's specialization
"""
@extend_schema(tags=["Specialization OF Doctor"])
class SpecializationViewSet(BaseDoctorViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


"""
review of doctor by patient but not by self
"""
@extend_schema(tags=["Review OF Doctor"])
class ReviewViewSet(BaseDoctorViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsVerifiedUser, 
        IsOwnerOrReadOnly, 
        permissions.IsAuthenticated, 
        IsNotReviewingSelf
    ]
    
    def perform_create(self, serializer):
        patient = getattr(self.request.user, 'patient', None)
        doctor_id = self.request.data.get('doctor')

        # Prevent multiple reviews for same doctor by same patient
        if Review.objects.filter(reviewer=patient, doctor_id=doctor_id).exists():
            raise serializers.ValidationError("You have already reviewed this doctor.")

        serializer.save(reviewer=patient)



"""
apply for add qualification of doctor
"""
@extend_schema(tags=["Qualifications OF Doctor"])
class QualificationApplyView(APIView):
    serializer_class = QualificationApplySerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsDoctor]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Submitted."}, status=201)
        return Response(serializer.errors, status=400)


"""
This API endpoint gets a doctor's qualifications.
It returns all qualifications for the authenticated and verified users.
thought no one can change it without admin him self
"""
@extend_schema(tags=["Qualifications OF Doctor"])
class DoctorQualificationsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def get(self, request, doctor_id):
        qs = Qualification.objects.filter(doctor_id=doctor_id, verification_status='APPROVED')
        serializer = DoctorQualificationsSerializer(qs, many=True)
        return Response(serializer.data)