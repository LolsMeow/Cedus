from django.db import models
from django.core.validators import MinValueValidator
import datetime
from django.contrib.auth.models import User
from decimal import *


# Patient class
class Patient(models.Model):
    u_name = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)  # pull from django user object
    p_f_name = models.CharField(max_length=50)
    p_l_name = models.CharField(max_length=50)
    p_dob = models.DateField()
    p_ph_num = models.CharField(max_length=50)  # convert into integer when necessary (make parser)
    p_gender = models.CharField(max_length=10)  # Male, Female, Other
    p_st_addr = models.CharField(max_length=50)
    p_apt = models.CharField(max_length=50)
    p_city = models.CharField(max_length=50)
    p_state = models.CharField(max_length=50)
    p_zip = models.IntegerField()
    p_language = models.CharField(max_length=50)

    # user_class field

    def __str__(self):
        return self.u_name.username


# Staff class
class Staff(models.Model):
    u_name = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)  # pull from django user object
    s_f_name = models.CharField(max_length=50)
    s_l_name = models.CharField(max_length=50)
    s_affiliation = models.CharField(max_length=100)

    # user_class field

    def __str__(self):
        return self.u_id.username


# Vitals class - each object represents one day of vital readings for a single patient
class Vitals(models.Model):
    vt_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    vt_date = models.DateField()
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)  # pull from django user object
    vt_bloodgroup = models.CharField(max_length=50)
    vt_bp_sys = models.IntegerField()  # systole
    vt_bp_dia = models.IntegerField()  # diastole
    vt_wbc = models.IntegerField()
    vt_rbc = models.DecimalField(max_digits=4, decimal_places=2)
    vt_height = models.DecimalField(max_digits=5, decimal_places=2)
    vt_weight = models.DecimalField(max_digits=6, decimal_places=2)
    vt_comments = models.CharField(max_length=400, default='', blank=True)


# Vaccine class - each object represents one vaccination on a single day for a single patient
class Vaccines(models.Model):
    vac_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)  # pull from django user object
    # doc_id = models.IntegerField() #we'll pull this from API
    vac_date = models.DateField()
    vac_type = models.CharField(max_length=100)
    vac_comment = models.CharField(max_length=400)


# Diagnosis class - each object represents one diagnosis on a single day for a single patient
class Diagnosis(models.Model):
    diagnosis_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)  # pull from django user object
    # doc_id = models.IntegerField() #we'll pull this from API
    diagnosis_date = models.DateField()
    diagnosis_status = models.CharField(max_length=100)
    diagnosis_comment = models.CharField(max_length=500)


# Prescription class - each object represents one prescription given by one provider to one patient
# NOTE: Must be connected to a diagnosis entry!
class Prescription(models.Model):
    rx_no = models.PositiveIntegerField(primary_key=True,
                                        validators=[MinValueValidator(10000)])  # minimum 5 digits long
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)  # pull from django user object
    diagnosis_no = models.IntegerField()
    rx_date = models.DateField()
    rx_name = models.CharField(max_length=100)
    rx_dosage = models.CharField(max_length=100)
    rx_sig = models.CharField(max_length=300)
    # doc_id = models.IntegerField() #we'll pull this from API
    rx_comments = models.CharField(max_length=100)


# Physician's Orders class - each object represents one order by a physician on a single day
# NOTE: Connected with Vitals, Vaccines, Diagnosis and Prescriptions
class Phys_Orders(models.Model):
    order_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    # all except for u_name is allowed to be blank: DO NOT HAVE TO CONNECT PHYS ORDERS WITH ANOTHER ENTRY
    order_date = models.DateField()
    orders = models.CharField(max_length = 500)


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    # doc_id = models.IntegerField() #we'll pull this from API
    appointment_date = models.DateField()
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)  # search by patient
    # appointment_loc = models.CharField(max_length=100) #we'll pull from API
    appointment_comments = models.CharField(max_length=100)


class Surgeries(models.Model):
    surgery_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)
    # doc_id = models.IntegerField() #we'll pull this from API
    surgery_date = models.DateField()
    # surgery_loc_id = models.IntegerField #we'll pull this from API
    surgery_description = models.CharField(max_length=100)


class Insurance(models.Model):
    ins_mem_id = models.CharField(max_length=20, primary_key=True)  # patient's insurance member ID
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)
    ins_name = models.CharField(max_length=100)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    ins_plan = models.CharField(max_length=100)
    ins_rx_bin = models.CharField(max_length=10)
    ins_rx_pcn = models.CharField(max_length=10)
    ins_rx_group = models.CharField(max_length=20)
    ins_coverage = models.CharField(max_length=100)


class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_date = models.DateField()
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
    pay_id = models.AutoField(primary_key=True) # auto-iterating index as primary key
    pay_date = models.DateField()
    pay_amount = models.DecimalField(max_digits=6, decimal_places=2)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    pay_description = models.CharField(max_length=100)
    pay_location = models.CharField(max_length=100)
