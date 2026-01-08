"""
BASE/base_views.py
"""
from rest_framework import generics

# from BASE permissions
from BASE.base_permissions import (
    IsVerifiedUser, 
    IsOwnerOrReadOnly
)
from BASE.base_pagination import BasePagination
from rest_framework.permissions import IsAuthenticated


# for doctor views
class BaseDoctorViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser, IsOwnerOrReadOnly]
    pagination_class = BasePagination
