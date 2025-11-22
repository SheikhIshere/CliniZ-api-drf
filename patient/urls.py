from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, 
    UserRegistrationApiView,
    activating_account,
    UserLogInApiView,
    UserLogOutApiView
)

router = DefaultRouter()
router.register(r'list', PatientViewSet, basename='patient')

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