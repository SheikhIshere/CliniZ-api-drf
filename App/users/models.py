"""
users/models.py
"""
# core imports
from django.db import models
# user manager & user
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin, 
    UserManager
)
# import role choice
from BASE.base_choice import Role
# import timezone
from django.utils import timezone

"""
user manager
explain: this class will help to create 
custom user and manage the user creation
"""
class AccountManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


"""
user model
explain: this class will help to create 
custom user and manage the user creation
"""
class User(AbstractBaseUser, PermissionsMixin):
    # the main authentication field
    email = models.EmailField(unique=True)

    # user status to admin
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # user role
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.PATIENT)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user manager
    objects = AccountManager()

    # user manager fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


"""
otp model
"""
class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    attempt = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'email: {self.user.email} - otp: {self.otp} - created at: {self.created_at}'
    





















