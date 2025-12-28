"""
BASE/base_choice.py
"""
# core import
from http.client import ACCEPTED
from django.db.models import IntegerChoices, TextChoices

# Role choices for user authentication
class Role(TextChoices):
    DOCTOR = 'doctor', 'Doctor'
    PATIENT = 'patient', 'Patient'
    ADMIN = 'admin', 'Admin'


# Gender choices for BaseProfile
class GenderChoice(TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'


# doctor section
class DoctorVerificationStatus(TextChoices):    
    PENDING = 'pending', 'Pending'
    APPROVED = 'verified', 'Verified'
    REJECTED = 'rejected', 'Rejected'


# doctor personal status
class DoctorPersonalStatus(TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    ON_LEAVE = 'on_leave', 'On Leave'


# doctor review star
class StarRating(IntegerChoices):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5



# appointment status
class AppointmentStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    RUNNING = 'running', 'Running'
    COMPLETED = 'completed', 'Completed'


# appointment type
class AppointmentType(TextChoices):
    ONLINE = 'online', 'Online'
    OFFLINE = 'offline', 'Offline'


# adminportal bug report
class BugType(TextChoices):
    UI = 'UI/UX', 'User Interface'
    FUNCTIONAL = 'Functional', 'Functional'
    PERFORMANCE = 'Performance', 'Performance'
    SECURITY = 'Security', 'Security'
    COMPATIBILITY = 'Compatibility', 'Compatibility'
    ACCESSIBILITY = 'Accessibility', 'Accessibility'
    NETWORK = 'Network', 'Network'
    DATABASE = 'Database', 'Database'
    INTEGRATION = 'Integration', 'Integration'
    OTHER = 'Other', 'Other'



class BugReportStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    RESOLVED = 'resolved', 'Resolved'
    REJECTED = 'rejected', 'Rejected'


# migrate profile status
class MigrateProfileStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
