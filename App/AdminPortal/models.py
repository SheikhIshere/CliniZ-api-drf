"""
AdminPortal/models.py
"""
# core import
from django.db import models
# base
from BASE.base_model import BaseModel
from BASE.base_choice import BugType, BugReportStatus
# user
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.

class ContactUs(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    problem = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.user.full_name or self.user.email




class ReportBug(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bug_type = models.CharField(max_length=50, choices=BugType.choices)
    bug_other = models.CharField(max_length=100, blank=True)
    issue = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='web_portal/bug_report/images', blank=True, null=True)

    status = models.CharField(max_length=20, choices=BugReportStatus.choices, default=BugReportStatus.PENDING)

    class Meta:
        verbose_name = 'Report Bug'
        verbose_name_plural = 'Report Bugs'

    def save(self, *args, **kwargs):
        # TODO: will add a email system that will tell the user his report has been submitted
        # TODO: will get update if issue is resolved and thank user
        super().save(*args, **kwargs)



class Service(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='web_portal/service/images')

    def __str__(self):
        return self.name        

