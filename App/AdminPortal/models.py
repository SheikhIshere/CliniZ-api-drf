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
    name = models.CharField(max_length=30, default='Guest')    
    email = models.EmailField(default='support@example.com')
    subject = models.CharField(max_length=100, null=True, blank=True)
    problem = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f"{self.first_name} {self.last_name}  {self.subject} "




class ReportBug(BaseModel):
    email = models.EmailField()
    bug_type = models.CharField(max_length=50, choices=BugType.choices)
    bug_other = models.CharField(max_length=100, blank=True)
    issue = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='web_portal/bug_report/images')

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

