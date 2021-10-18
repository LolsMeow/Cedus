from django.db import models
from datetime import datetime
from decimal import *


class User_Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=100)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=100)
    phone_num = models.IntegerField()
    role_id = models.ForeignKey(User_Role, on_delete=models.CASCADE, related_name='role_id_U')


class Patient(models.Model):
    p_id = models.IntegerField(primary_key=True)
    p_f_name = models.CharField(max_length=100)
    p_l_name = models.CharField(max_length=100)
    p_dob = models.DateField()
    p_gender = models.CharField(max_length=100)
    p_city = models.CharField(max_length=100)
    p_state = models.CharField(max_length=100)
    p_zipcode = models.IntegerField()
    p_language = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id_P')


class Staff(models.Model):
    s_id = models.IntegerField(primary_key=True)
    s_f_name = models.CharField(max_length=100)
    s_l_name = models.CharField(max_length=100)
    s_affiliation = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id_S')
    role_id = models.ForeignKey(User_Role, on_delete=models.CASCADE, related_name='role_id_S')


class Allergies(models.Model):
    aller_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_A')
    #doc_id = models.Integerfield() #we'll pull this from API
    aller_to = models.CharField(max_length=100)
    aller_comments = models.CharField(max_length=100)


class Vitals(models.Model):
    vt_no = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_V')
    vt_date = models.DateField()
    vt_bloodgroup = models.CharField(max_length=100)
    vt_bp_sys = models.IntegerField() #systole
    vt_bp_dia = models.IntegerField() #diastole
    vt_wbc = models.IntegerField()
    vt_rbc = models.IntegerField()
    vt_height = models.DecimalField(max_digits=3, decimal_places=2)
    vt_weight = models.DecimalField(max_digits=4, decimal_places=2)
    vt_comments = models.CharField(max_length=100)


class Vaccines(models.Model):
    vac_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_Vac')
    #doc_id = models.IntegerField() #we'll pull this from API
    vac_date = models.DateField()
    vac_type = models.CharField(max_length=100)
    vac_comment = models.CharField(max_length=100)


class Diagnosis(models.Model):
    diagnosis_no = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_Diag')
    # doc_id = models.IntegerField() #we'll pull this from API
    diagnosis_date = models.DateField()
    diagnosis_status = models.CharField(max_length=100)
    diagnosis_comment = models.CharField(max_length=100)


class Prescription(models.Model):
    rx_no = models.IntegerField(primary_key=True)
    diagnosis_no = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='diag_no_rx')
    rx_date = models.DateField()
    rx_dosage = models.CharField(max_length=100)
    rx_comments = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id_rx')


class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    #doc_id = models.IntegerField() #we'll pull this from API
    appointment_date = models.DateField()
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_Appo')
    appointment_loc = models.CharField(max_length=100)
    appointment_comments = models.CharField(max_length=100)


class Surgeries(models.Model):
    surgery_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_S')
    # doc_id = models.IntegerField() #we'll pull this from API
    surgery_date = models.DateField()
    #surgery_loc_id = models.IntegerField #we'll pull this from API
    surgery_description = models.CharField(max_length=100)


class Insurance(models.Model):
    ins_mem_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_Ins')
    ins_name = models.CharField(max_length=100)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    ins_plan = models.CharField(max_length=100)
    ins_rx_bin = models.CharField(max_length=10)
    ins_rx_pcn = models.CharField(max_length=10)
    ins_rx_group = models.CharField(max_length=20)
    ins_coverage = models.CharField(max_length=100)


class Bills(models.Model):
    bill_id = models.IntegerField(primary_key=True)
    p_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='p_id_B')
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
    pay_id = models.IntegerField(primary_key=True)
    bill_id = models.ForeignKey(Bills, on_delete=models.CASCADE, related_name = 'bill_id_P')
    pay_date = models.DateField()
    pay_amount = models.DecimalField(max_digits=6, decimal_places=2)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    pay_description = models.CharField(max_length=100)
    pay_location = models.CharField(max_length=100)
