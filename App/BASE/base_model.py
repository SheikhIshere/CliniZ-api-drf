"""
BASE/base_model.py
"""

# core imports
import uuid
from django.db import models
from django.utils.text import slugify


# user import
from django.contrib.auth import get_user_model
User = get_user_model()

# local imports
from .base_choice import (
    GenderChoice
)

"""
base model for all model
"""
class BaseModel(models.Model):
    """Base model with common fields for all models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


"""
User profile base model
Defines common fields and methods for user profile models
"""
class BaseProfile(BaseModel):
    # id: for security i am using uuid4 as id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # main user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # personal information
    full_name = models.CharField(max_length=255, blank=True)
    photo = None
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(
        choices=GenderChoice.choices, 
        max_length=10, 
        blank=True, null=True, 
        default=GenderChoice.OTHER
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True)
    height = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, null=True, 
        help_text="height in inches"
    )
    weight = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        blank=True, null=True, 
        help_text="weight in kg"
    )

    # contact information
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    # for admin use
    token = models.PositiveBigIntegerField(blank=True, null=True, default=0)

    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.birthday:
            import datetime
            today = datetime.date.today()
            self.age = today.year - self.birthday.year - (
                (today.month, today.day) < (self.birthday.month, self.birthday.day)
            )
        super().save(*args, **kwargs)





"""
doctor attribute base model
"""
class DoctorAttribute(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(
        max_length=255, 
        null=True, blank=True, 
        help_text="This will be auto filled when it saved"
    )
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        abstract = True

    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)





