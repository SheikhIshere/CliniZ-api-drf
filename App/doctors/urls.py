from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorListView,
    DoctorMeView,
    DoctorsProfile,
    AvailableTimeViewSet,
    # AvailableTimeForPatientViewSet,
    DesignationViewSet,
    SpecializationViewSet,
    QualificationApplyView,
    DoctorQualificationsView,
    DoctorQualificationsSingleView,
    ReviewViewSet,
)

router = DefaultRouter()
# router.register("available-times", AvailableTimeViewSet, basename="available-time")
# router.register("available-times-patient", AvailableTimeForPatientViewSet, basename="available-time-patient")
# router.register("designations", DesignationViewSet, basename="designation")
# router.register("specializations", SpecializationViewSet, basename="specialization")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),    
    
    path('available-times/', AvailableTimeViewSet.as_view(), name="available-time"),
    path('designations/', DesignationViewSet.as_view(), name="designation"),
    path('specializations/', SpecializationViewSet.as_view(), name="specialization"),
            
    path('list/', DoctorListView.as_view(), name='doctor-list'),    
    path("profile/me/", DoctorMeView.as_view(), name="doctor-me"),
    path("profile/<str:user__email>", DoctorsProfile.as_view(), name="doctor-profile"),
    path("<uuid:doctor__id>/qualifications/", DoctorQualificationsView.as_view(), name='doctor-qualifications'),
    path("qualifications/<int:pk>", DoctorQualificationsSingleView.as_view(), name='doctor-single-qualifications'),
    path("qualifications/apply/", QualificationApplyView.as_view(), name="qualification-apply"),
]



