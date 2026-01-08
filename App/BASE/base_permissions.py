"""
here i am defining custom permission
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS 
from BASE.base_choice import Role

""" 
User who is verified only can access the resource.
"""
class IsVerifiedUser(BasePermission):
    """
    Allows access only to users with is_verified=True.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_verified)


"""
Custom permission to only allow owners of an object to edit it.
"""
class IsOwnerOrReadOnly(BasePermission):
    """
    Anyone can retrieve (GET).
    Only the owner can update or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and getattr(obj, 'user', None) == request.user)


"""
a doctor cannot review other doctor and self as well 
so this will be prevent other including himself(doctor)
from reviewing, else will be vai_chara at top :)
"""
class IsNotReviewingSelf(BasePermission):    
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role == 'doctor':
                return False
        return True


class IsMeDoctor(BasePermission):
    """
    Allow access only if the user is a doctor.
    Works for all request methods.
    """
    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Only allow if user role is doctor
        return user.role == Role.DOCTOR    
    


"""
checking is user who trying to do request is he doctor or not for 
applying permission to add a certificate in his account
"""      
class IsDoctor(IsMeDoctor): # FIX: cannot change soo much is doctor fast so just doing inherit
    """
    Allow access only if the user is a doctor.
    """
    # def has_permission(self, request, view):
    #     if request.method == 'POST':
    #         return request.user.role == Role.DOCTOR
    #     return False  # Allow other methods for doctors as well
    

class IsPatient(BasePermission):
    """
    Allow access only if the user is a patient.
    """
    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Only allow if user role is patient
        return user.role == Role.PATIENT