from django.urls import path, include
from rest_framework.routers import DefaultRouter


# views import 
# from doctor
from doctor.views import (
    DoctorViewSet,
    AvailableTimeViewSet,
    DesignationViewSet,
    SpecializationViewSet,
    ReviewViewSet
)
# from appointment
from appointment.views import AppointmentViewSet
# from contact_us
from contact_us.views import ContactUsViewSet
# from patient
from patient.views import (
    PatientViewSet, 
    UserRegistrationApiView,
    activating_account,
    UserLogInApiView,
    UserLogOutApiView
)
# from service
from service.views import ServiceViewSet


router = DefaultRouter()

# from doctor.views 
router.register(r'doctor-list', DoctorViewSet, basename='doctor')
router.register(r'available_time', AvailableTimeViewSet, basename='available_time')
router.register(r'designation', DesignationViewSet, basename='designation')
router.register(r'specialization', SpecializationViewSet, basename='specialization')
router.register(r'review', ReviewViewSet, basename='review')

# from appointment.views
router.register(r'appointment-list', AppointmentViewSet, basename='appointment')

# from contact_us.views
router.register(r'contact_us-list', ContactUsViewSet, basename='contact_us')

# from patient.views
router.register(r'patient-list', PatientViewSet, basename='patient')

# from service.views
router.register(r'service-list', ServiceViewSet, basename='service')




urlpatterns = [
    path('', include(router.urls)),
    path('registration/', 
         UserRegistrationApiView.as_view(), 
         name='registration'),
    path(
        'activate/<uidb64>/<token>', 
        activating_account, 
        name='activate'
    ),
    path('login/', UserLogInApiView.as_view(), name='login'),
    path('logout/', UserLogOutApiView.as_view(), name='logout'),
]






