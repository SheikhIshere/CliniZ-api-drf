from django.db import models

# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    problem = models.TextField()

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.name