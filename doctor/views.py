from rest_framework import (
    viewsets,
    filters,
    pagination
)

from .models import (
    Doctor, 
    AvailableTime, 
    Designation, 
    Specialization,
    Review
)
from .serializers import (
    DoctorSerializer, 
    AvailableTimeSerializer, 
    DesignationSerializer, 
    SpecializationSerializer,
    ReviewSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class DoctorPagination(pagination.PageNumberPagination):
    page_size = 1 # this represent's data per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = DoctorPagination
    search_fields = [
        'user__first_name', 'user__last_name', 
        'designation__name', 'specialization__name', 
        'user__email'
    ]


class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(doctor=doctor_id)
        return queryset
    
class AvailableTimeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer    
    filter_backends = [AvailableTimeForSpecificDoctor]

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



