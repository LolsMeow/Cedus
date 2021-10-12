from django.db import models
from datetime import datetime

# Create your models here.
class Patient(models.Model):
    P_FullName = models.CharField(max_length=50)
    P_DOB = models.DateField()
    P_Gender = models.CharField(max_length=50)
    P_Address = models.CharField(max_length=50)
    P_City = models.CharField(max_length=50)
    P_State = models.CharField(max_length=50)
    P_Language = models.CharField(max_length=50)