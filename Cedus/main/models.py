from django.db import models
import datetime
from django.contrib.auth.models import User
from decimal import *


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    birth_date = models.DateField(default=datetime.date.today)
    phone_number = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    apt = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()

    provider_name = models.CharField(max_length=50)
    plan_name = models.CharField(max_length=50)
    rx_bin = models.IntegerField()
    id_number = models.IntegerField()
    rx_pcn = models.CharField(max_length = 5)
    rx_group = models.CharField(max_length=50)

    gender = models.CharField(max_length=10, blank=True)  # Male, Female, Nonbinary
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Insurance(models.Model):
    ins_mem_id = models.CharField(max_length=20, primary_key=True)  # patient's insurance member ID
    u_name = models.CharField(max_length=50)
    ins_name = models.CharField(max_length=100)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    ins_plan = models.CharField(max_length=100)
    ins_rx_bin = models.CharField(max_length=10)
    ins_rx_pcn = models.CharField(max_length=10)
    ins_rx_group = models.CharField(max_length=20)
    ins_coverage = models.CharField(max_length=100)



class Allergies(models.Model):
    aller_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=50, blank=True)
    aller_drug = models.CharField(max_length=20)
    aller_severity = models.CharField(max_length=10)

# Staff class
class Staff(models.Model):
    u_name = models.CharField(max_length=50)  # pull from django user object
    s_f_name = models.CharField(max_length=50)
    s_l_name = models.CharField(max_length=50)
    s_affiliation = models.CharField(max_length=100)


class Vitals(models.Model):
    vt_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # pull from django user object
    vt_bloodgroup = models.CharField(max_length=50)
    vt_bp_sys = models.IntegerField()  # systole
    vt_bp_dia = models.IntegerField()  # diastole
    vt_wbc = models.IntegerField()
    vt_rbc = models.DecimalField(max_digits=4, decimal_places=2)
    vt_height = models.DecimalField(max_digits=5, decimal_places=2)
    vt_weight = models.DecimalField(max_digits=6, decimal_places=2)
    vt_comments = models.CharField(max_length=400, default='', blank=True)


# Diagnosis class - each object represents one diagnosis on a single day for a single patient
class Diagnosis(models.Model):
    diagnosis_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # pull from django user object
    diagnosis_date = models.DateField()
    diagnosis_status = models.CharField(max_length=100)
    diagnosis_comment = models.CharField(max_length=500)


# Physician's Orders class - each object represents one order by a physician on a single day
# NOTE: Connected with Vitals, Vaccines, Diagnosis and Prescriptions
class Phys_Orders(models.Model):
    order_no = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)
    order_date = models.DateField()
    order_contents = models.CharField(max_length=500)


# Prescription class - each object represents one prescription given by one provider to one patient
# NOTE: Must be connected to a diagnosis entry!
class Prescription(models.Model):
    rx_no = models.PositiveIntegerField(primary_key=True)
    u_name = models.CharField(max_length=50)
    rx_date = models.DateField()
    rx_name = models.CharField(max_length=100)
    rx_dosage = models.CharField(max_length=100)
    rx_sig = models.CharField(max_length=300)  # drug instructions
    rx_comments = models.CharField(max_length=100)


# Vaccine class - each object represents one vaccination on a single day for a single patient
class Vaccines(models.Model):
    vac_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # pull from django user object
    vac_date = models.DateField()
    vac_type = models.CharField(max_length=100)
    vac_comment = models.CharField(max_length=400)


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    appointment_date = models.DateField()
    u_name = models.CharField(max_length=50)  # search by patient
    appointment_comments = models.CharField(max_length=400)


class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # search by patient
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
    u_name = models.CharField(max_length=50)
    pay_date = models.DateField()
    pay_amount = models.DecimalField(max_digits=6, decimal_places=2)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2)
    pay_description = models.CharField(max_length=100)
    pay_location = models.CharField(max_length=100)
