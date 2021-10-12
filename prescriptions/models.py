from django.db import models

# Create your models here.
class Presciption(models.Model):
    Pr_Date = models.DateField()
    Pr_Medication = models.CharField(max_length=50)
    Pr_Comments = models.CharField(max_length=50)