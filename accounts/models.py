from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
