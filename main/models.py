from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    birth_date = models.DateField(default=datetime.date.today)
    phone_number = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    apt = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$')])

    provider_name = models.CharField(max_length=50, blank=True, null=True)
    plan_name = models.CharField(max_length=50, blank=True, null=True)
    rx_bin = models.IntegerField(blank=True, null=True)
    id_number = models.IntegerField(blank=True, null=True)
    rx_pcn = models.CharField(max_length=10, blank=True, null=True,)
    rx_group = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.user.username

class Insurance(models.Model):
    #ins_mem_id = models.CharField(max_length=20, primary_key=True, default=1)  # patient's insurance member ID
    u_name = models.CharField(max_length=50)
    ins_name = models.CharField(max_length=100, blank=True, null=True)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ins_plan = models.CharField(max_length=100, blank=True, null=True)
    ins_rx_bin = models.CharField(max_length=10, blank=True, null=True)
    ins_rx_pcn = models.CharField(max_length=10, blank=True, null=True)
    ins_rx_group = models.CharField(max_length=20, blank=True, null=True)
    ins_coverage = models.CharField(max_length=100, blank=True, null=True)



class Allergies(models.Model):
    #aller_id = models.AutoField(primary_key=True, default=1)
    u_name = models.CharField(max_length=50, blank=True, null=True)
    aller_drug = models.CharField(max_length=20, blank=True, null=True)
    aller_severity = models.CharField(max_length=10, blank=True, null=True)

# Staff class
class Staff(models.Model):
    u_name = models.CharField(max_length=50)  # pull from django user object
    s_f_name = models.CharField(max_length=50, blank=True, null=True)
    s_l_name = models.CharField(max_length=50, blank=True, null=True)
    s_affiliation = models.CharField(max_length=100, blank=True, null=True)


class Vitals(models.Model):
    #vt_no = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # pull from django user object
    vt_date = models.DateField(blank=True, null=True)
    vt_bloodgroup = models.CharField(max_length=50, blank=True, null=True)
    vt_bp_sys = models.IntegerField(blank=True, null=True)  # systole
    vt_bp_dia = models.IntegerField(blank=True, null=True)  # diastole
    vt_wbc = models.IntegerField(blank=True, null=True)
    vt_rbc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    vt_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vt_weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vt_comments = models.CharField(max_length=400, default='',blank=True, null=True)


# Diagnosis class - each object represents one diagnosis on a single day for a single patient
class Diagnosis(models.Model):
    #diagnosis_no = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # pull from django user object
    diagnosis_date = models.DateField(blank=True, null=True)
    diagnosis_status = models.CharField(max_length=100, blank=True, null=True)
    diagnosis_comment = models.CharField(max_length=500, blank=True, null=True)


# Physician's Orders class - each object represents one order by a physician on a single day
# NOTE: Connected with Vitals, Vaccines, Diagnosis and Prescriptions
class Phys_Orders(models.Model):
    #order_no = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)
    order_date = models.DateField(blank=True, null=True)
    order_contents = models.CharField(max_length=500, blank=True, null=True)


# Prescription class - each object represents one prescription given by one provider to one patient
# NOTE: Must be connected to a diagnosis entry!
class Prescription(models.Model):
    #rx_no = models.PositiveIntegerField(primary_key=True, default=1)
    u_name = models.CharField(max_length=50)
    rx_date = models.DateField(blank=True, null=True)
    rx_name = models.CharField(max_length=100, blank=True, null=True)
    rx_dosage = models.CharField(max_length=100, blank=True, null=True)
    rx_sig = models.CharField(max_length=300, blank=True, null=True)  # drug instructions
    rx_comments = models.CharField(max_length=100, blank=True, null=True)


# Vaccine class - each object represents one vaccination on a single day for a single patient
class Vaccines(models.Model):
    #vac_id = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50, blank=True, null=True)  # pull from django user object
    vac_date = models.DateField(blank=True, null=True)
    vac_type = models.CharField(max_length=100, blank=True, null=True)
    vac_comment = models.CharField(max_length=400, blank=True, null=True)


class Appointment(models.Model):
    #appointment_id = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    appointment_date = models.DateField(blank=True, null=True)
    u_name = models.CharField(max_length=50, blank=True, null=True)  # search by patient
    appointment_comments = models.CharField(max_length=400, blank=True, null=True)


class Bills(models.Model):
    #bill_id = models.AutoField(primary_key=True, default=1)  # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)  # search by patient
    charge_date = models.DateField(blank=True, null=True)
    doc_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    medi_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    room_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    surgery_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    admission_days = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    nursing_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    advance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    test_charges = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bill_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


class Payment(models.Model):
   #pay_id = models.AutoField(primary_key=True, default=1) # auto-iterating index as primary key
    u_name = models.CharField(max_length=50)
    pay_date = models.DateField(blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ins_copay = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    pay_description = models.CharField(max_length=100, blank=True, null=True)
    pay_location = models.CharField(max_length=100, blank=True, null=True)