"""
AdminPortal/views.py
"""
# core imports
from rest_framework import generics
from rest_framework.permissions import AllowAny

# local imports
from .models import ContactUs, Service, ReportBug
from .serializers import ContactUsSerializer, ServiceSerializer, ReportBugSerializer
from .serializers import ReviewSerializerPublic

# api documentation
from drf_spectacular.utils import extend_schema

# 
from doctors.views import DoctorListView
from doctors.models import Review

@extend_schema(tags=['user-feedback'], description="Create a new contact us entry")
class ContactUsListCreateView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['user-feedback'], description="List all report bugs or create a new one")
class ReportBugListCreateView(generics.CreateAPIView):
    queryset = ReportBug.objects.all()
    serializer_class = ReportBugSerializer



@extend_schema(tags=['website-decoration'], description="List all services")
class ServiceListCreateView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['website-decoration'], description="List all services")
class DoctorList(DoctorListView):
    permission_classes = [AllowAny]


@extend_schema(tags=['website-decoration'], description="doctor reviews")
class DoctorReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerPublic
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.exclude(body__isnull=True).exclude(body="").order_by("-star")



