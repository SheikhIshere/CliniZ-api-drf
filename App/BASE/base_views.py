"""
BASE/base_views.py
"""
from rest_framework import viewsets

# from BASE permissions
from BASE.base_permissions import (
    IsVerifiedUser, 
    IsOwnerOrReadOnly
)
from BASE.base_pagination import BasePagination
from rest_framework.permissions import IsAuthenticated


# for doctor views
class BaseDoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVerifiedUser, IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = BasePagination
