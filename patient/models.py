from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime
from rest_framework import serializers
from decimal import *


class User_Role(models.Model):
    role_id = models.IntegerField(default=1, primary_key=True)
    role = models.CharField(max_length=100, blank=True)

class User_Cedus(models.Model):
    user_id = models.IntegerField(default=1, primary_key=True)
    user_email = models.EmailField(blank=True)
    user_password = models.CharField(max_length=100, blank=True)
    phone_num = models.CharField(max_length=100, blank=True)
    role_id = models.ForeignKey(User_Role, on_delete=models.CASCADE)


class Patient(models.Model):
    p_id = models.IntegerField(default=1, primary_key=True)
    p_f_name = models.CharField(max_length=100, default='', blank=True)
    p_l_name = models.CharField(max_length=100, default='', blank=True)
    p_dob = models.DateField(default='', blank=True)
    p_gender = models.CharField(max_length=100, default='', blank=True)
    p_city = models.CharField(max_length=100, default='', blank=True)
    p_state = models.CharField(max_length=100, default='', blank=True)
    p_zipcode = models.IntegerField(default='', blank=True)
    p_language = models.CharField(max_length=100, default='', blank=True)
    user_id = models.ForeignKey(User_Cedus, on_delete=models.CASCADE)


class Staff(models.Model):
    s_id = models.IntegerField(primary_key=True, default='', blank=True)
    s_f_name = models.CharField(max_length=100, default='', blank=True)
    s_l_name = models.CharField(max_length=100, default='', blank=True)
    s_affiliation = models.CharField(max_length=100, default='', blank=True)
    user_id = models.ForeignKey(User_Cedus, on_delete=models.CASCADE)
    role_id = models.ForeignKey(User_Role, on_delete=models.CASCADE)


class Allergies(models.Model):
    aller_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doc_id = models.Integerfield() #we'll pull this from API
    aller_to = models.CharField(max_length=100)
    aller_comments = models.CharField(max_length=100)


class Vitals(models.Model):
    vt_no = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vt_date = models.DateField()
    vt_bloodgroup = models.CharField(max_length=100)
    vt_bp_sys = models.IntegerField()  # systole
    vt_bp_dia = models.IntegerField()  # diastole
    vt_wbc = models.IntegerField()
    vt_rbc = models.DecimalField(max_digits=4, decimal_places=2)
    vt_height = models.DecimalField(max_digits=5, decimal_places=2)
    vt_weight = models.DecimalField(max_digits=6, decimal_places=2)
    vt_comments = models.CharField(max_length=100,blank=True)


class Vaccines(models.Model):
    vac_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doc_id = models.IntegerField() #we'll pull this from API
    vac_date = models.DateField()
    vac_type = models.CharField(max_length=100)
    vac_comment = models.CharField(max_length=100)


class Diagnosis(models.Model):
    diagnosis_no = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doc_id = models.IntegerField() #we'll pull this from API
    diagnosis_date = models.DateField()
    diagnosis_status = models.CharField(max_length=100)
    diagnosis_comment = models.CharField(max_length=100)


class Prescription(models.Model):
    rx_no = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(11111)])
    diagnosis_no = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    rx_date = models.DateField()
    rx_dosage = models.CharField(max_length=100)
    rx_comments = models.CharField(max_length=100)
    user_id = models.ForeignKey(User_Cedus, on_delete=models.CASCADE)


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    # doc_id = models.IntegerField() #we'll pull this from API
    appointment_date = models.DateField()
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_loc = models.CharField(max_length=100)
    appointment_comments = models.CharField(max_length=100)


class Surgeries(models.Model):
    surgery_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doc_id = models.IntegerField() #we'll pull this from API
    surgery_date = models.DateField()
    # surgery_loc_id = models.IntegerField #we'll pull this from API
    surgery_description = models.CharField(max_length=100)


class Insurance(models.Model):
    ins_mem_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ins_name = models.CharField(max_length=100)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    ins_plan = models.CharField(max_length=100)
    ins_rx_bin = models.CharField(max_length=10)
    ins_rx_pcn = models.CharField(max_length=10)
    ins_rx_group = models.CharField(max_length=20)
    ins_coverage = models.CharField(max_length=100)


class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doc_charges = models.DecimalField(max_digits=6, decimal_places=2)
    medi_charges = models.DecimalField(max_digits=6, decimal_places=2)
    room_charges = models.DecimalField(max_digits=6, decimal_places=2)
    surgery_charges = models.DecimalField(max_digits=6, decimal_places=2)
    admission_days = models.DecimalField(max_digits=6, decimal_places=2)
    nursing_charges = models.DecimalField(max_digits=6, decimal_places=2)
    advance = models.DecimalField(max_digits=6, decimal_places=2)
    test_charges = models.DecimalField(max_digits=6, decimal_places=2)
    bill_amount = models.DecimalField(max_digits=6, decimal_places=2)


class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    bill_id = models.ForeignKey(Bills, on_delete=models.CASCADE)
    pay_date = models.DateField()
    pay_amount = models.DecimalField(max_digits=6, decimal_places=2)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    pay_description = models.CharField(max_length=100)
    pay_location = models.CharField(max_length=100)
