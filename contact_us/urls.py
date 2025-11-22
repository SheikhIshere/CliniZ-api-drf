from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ContactUsViewSet

router = DefaultRouter()
router.register(r'', ContactUsViewSet, basename='contact_us')

urlpatterns = [
    path('', include(router.urls)),
]