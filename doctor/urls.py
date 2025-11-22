from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet,
    AvailableTimeViewSet,
    DesignationViewSet,
    SpecializationViewSet,
    ReviewViewSet
)



router = DefaultRouter()
router.register(r'list', DoctorViewSet, basename='doctor')
router.register(r'available_time', AvailableTimeViewSet, basename='available_time')
router.register(r'designation', DesignationViewSet, basename='designation')
router.register(r'specialization', SpecializationViewSet, basename='specialization')
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
