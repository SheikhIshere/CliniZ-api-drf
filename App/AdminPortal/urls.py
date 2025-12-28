from django.urls import path
from .views import (
    ContactUsListCreateView,
    ReportBugListCreateView,
    ServiceListCreateView,
    DoctorList,
    DoctorReviewView
)

urlpatterns = [
    path('contact-us/', ContactUsListCreateView.as_view(), name='contact-us-create'),
    path('report-bug/', ReportBugListCreateView.as_view(), name='report-bug-create'),
    path('services/', ServiceListCreateView.as_view(), name='service-list'),
    path('list/doctor/', DoctorList.as_view(), name='public-doctor-list'),
    path('list/doctor/reviews/', DoctorReviewView.as_view(), name='public-doctor-review-list'),
]

