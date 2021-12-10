import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cedus.settings')

import django

django.setup()

import decimal
import random
from main import models
from main import views
from faker import Faker
from django.contrib.auth.models import User
import csv

fakegen = Faker()

allergy_list = ['ampicillin', 'aztreonam', 'cefotaxime', 'ceftazidime', 'ceftriaxone', 'ciprofloxacin',
                 'clindamycin', 'co-trimoxazole', 'daptomycin', 'enviomycin', 'ethambutol', 'imipenem/cilastin',
                 'isoniazid', 'linezolid', 'meropenem', 'metronidazole', 'penicillin', 'quinidine', 'rifampicin',
                 'streptomycin', 'sulphadiamine', 'sulphadiazine', 'tobramycin', 'vancomycin', 'fluconazole',
                 'itraconazole', 'acycolvir', 'amprenavir', 'darunavir', 'efavirenz', 'enfuvartide', 'nelfinavir',
                 'nevirapine', 'tipranavir', 'zidovudine', 'adalimumab', 'cetuximab', 'glatiramer acetate',
                 'infliximab', 'l-asparaginase', 'carboplatin', 'cisplatin', 'cytarabine', 'docetaxel',
                 'imatinib mesylate', 'lenalidomide', 'mechlorethamine', '6-mercaptopurine', 'oxaliplatin',
                 'paclitaxel', 'sunitinib', 'thalidomide', 'azathioprine', 'cyclosporine', 'dapsone',
                 'hydroxychloroquine', 'mesalazine', 'methotrexate', 'mycophenolate mofetil', 'd-peniciliamine',
                 'sulfasalazine', 'carbamazepine', 'oxcarbazepine', 'phenobarbital', 'phenytoin', 'anastrazole',
                 'corticotropine', 'follicle-stimulating hormone', 'growth hormone', 'insulin', 'antithymocyte ',
                 'globulin', 'allopurinol', '5-aminosalicylic acid', 'buprenorphine', 'calcitonin', 'clopidrogel',
                 'colchicine', 'desferrioxamine', 'enoxaparine', 'erythropoietin', 'ferrous compounds',
                 'fluorercein', 'fluoxetine', 'furosemide', 'heparin', 'imiglucerase', 'interferon', 'isonicotinic',
                 'acid hydrazine',  'methylphenidate', 'neuromuscular receptor', 'blockers', 'opioids',
                 'radiocontrast media', 'ubiquinone', 'warfarin']
severity_list = ['Low', 'Medium', 'High']
companies = ['Healthfirst', 'Medicaid', 'Medicare-PartD', 'Blue-Cross Blue-Shield', 'Cygna']
ins_plan_names = ['Class A', 'Class B', 'Class C', 'Silver', 'Gold']
coverage = ['Medical', 'Dental', 'Vision']

genders = ['Male', 'Female', 'Nonbinary']

condition = ['Heart disease', 'depression', 'type 2 diabetes', 'arthritis', 'asthma', 'COPD', 'chronic kidney']

#NOTE: BOTH LISTS SHOULD BE THE SAME SIZE
vaccine_list = ['BCG', 'Hep B', 'Polio', 'DTP', 'MMR']
vaccine_comments = ['Tuberculosis', 'Hepatitis B', 'Poliovirus', 'Diptheria, Tetanus, Pertussis', 'Measles, Mumps, Rubella']

appointment_types = ['Regular Checkup', 'Urgent Appointment', 'Follow-up', 'Vaccination', 'Bloodwork', 'Labwork']

# Creates a list or single element randomly to the number decided by user
#             list_ : iterable
#         numneeded : int number of items to be chosen randomly (if greater than size of list, numneeded = size of list)
#     numneeded = 0 : generates a random number of items to be chosen (DEFAULT SETTING)
#       allow_empty : allow the return of nothing (0 to n items) (BOOLEAN : DEFAULT IS FALSE)
def pickoutofhat(list_, num_needed=0, allow_empty=False):
    rng_list = []
    rng_set = set([])

    limit = 0

    # confirm the total number of items needed#####################
    # CASE 1: 0 input means random number, cannot return empty
    if (num_needed == 0 and allow_empty == False):
        limit = fakegen.random_int(min=1, max=len(list_), step=1)

    # Case 2: 0 input means random number, returning empty is allowed
    elif (num_needed == 0 and allow_empty == True):
        limit = fakegen.random_int(min=0, max=len(list_), step=1)
        # RETURN EMPTY scenario
        if (limit == 0):
            return rng_list

    # Case 3: number of items from param
    elif (num_needed > len(list_)):
        limit = len(list_)

    # Case 4: normal case
    else:
        limit = num_needed
    ###############################################################

    while len(rng_list) < limit:
        rng_index = fakegen.random_int(min=0, max=len(list_) - 1, step=1)
        # first item case
        if len(rng_list) == 0:
            rng_list.append(list_[rng_index])
            # make copy for duplication chest
            rng_set.add(list_[rng_index])
        # check for duplicates and then append
        if list_[rng_index] not in rng_set:
            rng_set.add(list_[rng_index])
            rng_list.append(list_[rng_index])

    if len(rng_list) == 1:
        return rng_list[0]

    else:
        return rng_list


## Makes a list to be used to fill Insurance object [7]
#   [0] = insurance member id - will be 12 digits
#   [1] = insurance name
#   [2] = insurance copay - between $0.00 and $50.00
#   [3] = insurance plan
#   [4] = insurance Rx Bin number -
#   [5] = insurance Rx PCN number - 3 upper letters
#   [6] = insurance Rx Group Number - 2 upper letters + 5 digits
#   [7] = insruance coverage
def make_ins():
    ins_mem_id = fakegen.random_int(min=100000000000000, max=999999999999999, step=1)
    ins_name = pickoutofhat(companies, 1, False)
    ins_copay = decimal.Decimal(str(round(random.uniform(0.00, 50.00), 2)))
    ins_plan = pickoutofhat(ins_plan_names, 1, False)
    ins_rx_bin = fakegen.random_int(min=100000, max=999999, step=1)
    ins_rx_pcn = str(fakegen.random_uppercase_letter()) + str(fakegen.random_uppercase_letter()) + str(
        fakegen.random_uppercase_letter())
    ins_rx_group = str(fakegen.random_uppercase_letter()) + str(fakegen.random_uppercase_letter()) + str(
        fakegen.random_int(min=10000, max=99999, step=1))
    ins_coverage = pickoutofhat(coverage, 0, True)

    return ins_mem_id, ins_name, ins_copay, ins_plan, ins_rx_bin, ins_rx_pcn, ins_rx_group, ins_coverage


## Makes a list to be used to fill Insurance object [
#   PASS IN OUTPUT FROM makes_ins()!
#   [0] = first_name (determined by gender)
#   [1] = last_name (determined by gender)
#   [2] = email
#   [3] = password
#   [4] = date of birth
#   [5] = phone number
#   [6] = street address
#   [7] = apartment number
#   [8] = city
#   [9] = state (abbreviation)
#  [10] = zipcode
#  [11] = provider name (OVERLAP WITH INS)
#  [12] = plan name (OVERLAP WITH INS)
#  [13] = rx bin (OVERLAP WTIH INS)
#  [14] = insurance id number (OVERLAP WITH INS)
#  [15] = rx pcn (OVERLAP WITH INS)
#  [16] = rx group (OVERLAP WTIH INS)
#  [17] = gender - Male, Female, Nonbinary
#  [18] = language
def make_pt(ins_obj):
    # gender determination 
    # 1 = male, 2 = female, 3 = Nonbinary
    gen_gender = pickoutofhat(genders, 1, False)
    gender = ''
    first_name = ''
    last_name = ''

    # male
    if gen_gender == 1:
        gender = 'M'
        first_name = fakegen.first_name_male()
        last_name = fakegen.last_name_male()
    # female
    elif gen_gender == 2:
        fk_p_gender = 'F'
        first_name = fakegen.first_name_female()
        last_name = fakegen.last_name_female()
    # nonbinary
    else:
        gender = 'NB'
        first_name = fakegen.first_name()
        last_name = fakegen.last_name()

    email = fakegen.email()
    password = fakegen.password(length=12)

    birth_date = fakegen.date_of_birth(minimum_age=18, maximum_age=100)
    phone_number = str(fakegen.phone_number())

    street_address = str(fakegen.street_address())
    apt = str(fakegen.random_int(min=1, max=25, step=1)) + str(fakegen.random_uppercase_letter())
    city = fakegen.city()
    state = fakegen.state_abbr()
    zip_code = fakegen.postcode_in_state(state)

    #provider_name = fakegen.name()

    plan_name = ins_obj[3]
    rx_bin = ins_obj[4]
    id_number = ins_obj[0]
    rx_pcn = ins_obj[5]
    rx_group = ins_obj[6]

    language = fakegen.language_name()

    return first_name, last_name, email, password, birth_date, phone_number, street_address, apt, city, state, \
           zip_code, plan_name, rx_bin, id_number, rx_pcn, rx_group, gender, language

## Makes a single instance of an allergy record
#   [0] aller_drug - drug or drug class patient is allergic to
#   [1] aller_severity - severity of the allergy
def make_allergy():
    aller_drug = pickoutofhat(allergy_list, 1, False)
    aller_severity = pickoutofhat(severity_list, 1, False)

    return aller_drug, aller_severity

## Makes a single instance of a vitals record
#   [0] vt_date
#   [1] vt_bloodgroup
#   [2] vt_bp_sys (bloodpressure Systole)
#   [3] vt_bp_dia (bloodpressure diastole)
#   [4] vt_wbc (white blood cell count)
#   [5] vt_rbc (red blood cell count)
#   [6] vt_height
#   [7] vt_weight
#   [8] vt_comments
def make_vital():
    vt_bloodgroup =''
    vt_date = fakegen.date()
    #decide blood group to reflect irl percentage of population
    blood_grp_num = fakegen.random_int(min=0, max=99, step=1)
    if 0 <= blood_grp_num <= 35:
        vt_bloodgroup = 'O+'
    elif 36 <= blood_grp_num <= 65:
        vt_bloodgroup = 'A+'
    elif 66 <= blood_grp_num <= 78:
        vt_bloodgroup = 'O-'
    elif 78 <= blood_grp_num <= 86:
        vt_bloodgroup = 'A-'
    elif 87 <= blood_grp_num <= 94:
        vt_bloodgroup = 'B+'
    elif 95 <= blood_grp_num <= 96:
        vt_bloodgroup = 'B-'
    elif 97 <= blood_grp_num <= 98:
        vt_bloodgroup = 'AB+'
    else:
        vt_bloodgroup = 'AB-'

    vt_bp_sys = 0
    vt_bp_dia = 0

    # deciding blood pressure based on percentage of population
    b_pressure_type = fakegen.random_int(min=0, max=99, step=1)
    if 0 <= b_pressure_type <= 46:
        # hyper tension
        vt_bp_sys = fakegen.random_int(min=130, max=200, step=1)
        vt_bp_dia = fakegen.random_int(min=80, max=100, step=1)
    elif 47 <= b_pressure_type <= 96:
        # normal blood pressure
        vt_bp_sys = fakegen.random_int(min=91, max=129, step=1)
        vt_bp_dia = fakegen.random_int(min=61, max=79, step=1)
    else:
        # low blood pressure
        vt_bp_sys = fakegen.random_int(min=70, max=90, step=1)
        vt_bp_dia = fakegen.random_int(min=40, max=60, step=1)

    vt_wbc = 0
    vt_rbc = 0

    #set blood cell counts
    vt_wbc = fakegen.random_int(min=4500, max=11000, step=1)
    #this is parts per million (10^6)
    vt_rbc = decimal.Decimal(str(round(random.uniform(4.2, 6.1), 2)))

    #height in feet
    vt_height = decimal.Decimal(str(round(random.uniform(4.08, 6.50), 2)))

    #weight in lbs
    vt_weight = decimal.Decimal(str(round(random.uniform(100.00, 330.00), 2)))

    #comments
    vt_comments = fakegen.paragraph(nb_sentences=1),

    return vt_date, vt_bloodgroup, vt_bp_sys, vt_bp_dia, vt_wbc, vt_rbc, vt_height, vt_weight, vt_comments


## Makes a single instance of a diagnosis record
#   [0] diagnosis_date
#   [1] diagnosis_status
#   [2] diagnosis_comment
def make_diagnosis():
    diagnosis_date = fakegen.date()

    diagnosis_status = pickoutofhat(condition,1,False)

    diagnosis_comment = fakegen.paragraph(nb_sentences=1)

    return diagnosis_date, diagnosis_status,diagnosis_comment


## Makes a single instance of a physcians orders record
#   [0] order_date
#   [1] order_contents
def make_phys_order():
    order_date = fakegen.date()
    order_contents = fakegen.paragraph(nb_sentences=1)

    return order_date, order_contents

## Makes a single instance of a prescription record
#   [0] rx_date
#   [1] rx_name
#   [2] rx_dosage
#   [3] rx_sig
#   [4] rx_comments
def make_rx_order():
    rx_date = fakegen.date()
    #empty array
    drug_list = []

    #read csv file that has list of all drug names and make 1 dimensional list
    with open('drugs.csv') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            drug_list.append(row[0])

    rand = fakegen.random_int(min=0, max=len(drug_list) - 1, step=1)

    rx_name = drug_list[rand]
    rx_dosage = fakegen.random_int(10, 300, step=20)
    rx_sig = fakegen.paragraph(nb_sentences=1)
    rx_comments = fakegen.paragraph(nb_sentences=1)

    return rx_date, rx_name, rx_dosage, rx_sig, rx_comments

## Makes a single instance of a vaccination record
# PASS IN VACCINE INDEX NUMBER
#   [0] vac_date
#   [1] vac_type
#   [2] vac_comment
def make_vac_record(index_num_here):
    vac_date = fakegen.date()
    vac_type = vaccine_list[index_num_here]
    vac_comment = vaccine_comments[index_num_here]

    return vac_date, vac_type, vac_comment

## Makes a single instance of an appointment
# Pass in user object?
#   [0] appointment_date
#   [1] appointment_comments (gives type of appointment)
def make_appointment():
    appointment_date = fakegen.date()

    rand = fakegen.random_int(min=0, max=len(appointment_types) - 1, step=1)
    appointment_comments = appointment_types[rand]

    return appointment_date, appointment_comments


## Makes a single instance of a bill record
#   [0] charge_date
#   [1] doc_charges
#   [2] medi_charges
#   [3] room_charges
#   [4] surgery_charges
#   [5] admission_days
#   [6] nursing_charges
#   [7] advance
#   [8] test_charges
#   [9] bill_amount
def make_bill():
    charge_date = fakegen.date()
    doc_charges = decimal.Decimal(str(round(random.uniform(0.00, 150.00), 2)))
    medi_charges = decimal.Decimal(str(round(random.uniform(10.00, 150.00), 2)))
    admission_days = fakegen.random_int(min=1,max=10,step=1)
    inpatient_cost = admission_days * 35.00
    surgery_charges = decimal.Decimal(str(round(random.uniform(500.00, 2000.00), 2)))
    room_charges = format(inpatient_cost, '.2f')
    nursing_cost = admission_days * 15.75
    nursing_charges = format(nursing_cost, '.2f')
    advance = decimal.Decimal(str(round(random.uniform(10.00, 150.00), 2)))
    test_charges = decimal.Decimal(str(round(random.uniform(20.00, 50.00), 2)))
    total = float(doc_charges) + float(medi_charges) + float(room_charges) + float(nursing_charges) + float(advance) + float(test_charges)
    bill_amount = format(total, '.2f')
    pay_date = charge_date
    pay_amount = random.uniform(0, total)
    ins_copay = random.uniform(0, 100)
    balance = total - (pay_amount + ins_copay)

    return charge_date, doc_charges, medi_charges, room_charges, surgery_charges, admission_days, nursing_charges, \
           advance, test_charges, bill_amount, pay_date, pay_amount, ins_copay, balance



def populate(number_of_profiles):

    for a in range(0, number_of_profiles):
        #insurance array
        this_ins = make_ins()
        #patient array
        this_pt = make_pt(this_ins)
        #fix fields in both arrays
        USER_NAME = str(this_pt[2])

        #make user
        user_ = User.objects.create_user(username=this_pt[2], email=this_pt[2], password= this_pt[3], first_name=this_pt[0],
                         last_name=this_pt[1])

        ############ MAKING INSURANCE ############
        new_ins = models.Insurance(u_name=USER_NAME, ins_name=this_ins[1],
                                 ins_copay=this_ins[2], ins_plan=this_ins[3], ins_rx_bin=this_ins[4], ins_rx_pcn= this_ins[5], ins_rx_group=this_ins[6], ins_coverage=this_ins[7])


        ############ MAKING PATIENT ############ #NOTE: gender=this_pt[17], language=this_pt[18] removed due to models
        new_pt = models.Patient(user=user_, birth_date=this_pt[4], phone_number=this_pt[5], street_address=this_pt[6],
                                apt=this_pt[7], city=this_pt[8], state=this_pt[9], zip_code=this_pt[10])

        new_ins.save()
        new_pt.save()


        print('[Username: ' + USER_NAME + '] [Name: ' + str(this_pt[0]) + ' ' + str(this_pt[1])+'] [Pass: '+str(
            this_pt[3])+']')

        ############ MAKING ALLERGIES ############
        #decide number of allergies by percent
        allergy_token = fakegen.random_int(min=0, max=99, step=1)
        num_of_allergy = 0
        if 0 <= allergy_token <= 74:
            num_of_allergy = 0
        elif 75 <= allergy_token <= 90:
            num_of_allergy = 1
        elif 91 <= allergy_token <= 95:
            num_of_allergy = 2
        else:
            num_of_allergy = 3


        #loop through and make allergies
        for a in range(0,num_of_allergy):
            this_aller = make_allergy()
            new_aller = models.Allergies(u_name= USER_NAME, aller_drug=this_aller[0], aller_severity=this_aller[1])

            new_aller.save()


        ############ MAKING VITALS ############
        # generate number of vital readings
        vital_token = fakegen.random_int(min=5, max=20, step=1)
        for b in range(0, vital_token):
            this_vital = make_vital()
            new_vital = models.Vitals(u_name=USER_NAME, vt_date=this_vital[0], vt_bloodgroup=this_vital[1],
                                      vt_bp_sys=this_vital[2], vt_bp_dia=this_vital[3], vt_wbc=this_vital[4],
                                      vt_rbc=this_vital[5], vt_height=this_vital[6], vt_weight=this_vital[7],
                                      vt_comments=this_vital[8])

            new_vital.save()

        ############ MAKING DIAGNOSIS ############
        diag_token = fakegen.random_int(min=3, max=20, step=1)
        for c in range(0, diag_token):
            this_diag = make_diagnosis()
            new_diag = models.Diagnosis(u_name=USER_NAME, diagnosis_date=this_diag[0], diagnosis_status=this_diag[1],
                                        diagnosis_comment=this_diag[2])

            new_diag.save()


        ############ MAKING PHYSICIAN'S ORDERS ############
        phys_o_token = fakegen.random_int(min=0, max=10, step=1)
        for d in range(0,phys_o_token):
            this_phys = make_phys_order()
            new_phys = models.Phys_Orders(u_name=USER_NAME, order_date=this_phys[0], order_contents=this_phys[1])

            new_phys.save()


        ############ MAKING PRESCRIPTIONS ############
        rx_token = fakegen.random_int(min=2, max=20,step=1)
        rx_num_ = 100000

        for e in range(0,rx_token):
            this_rx = make_rx_order()
            new_rx = models.Prescription(u_name=USER_NAME, rx_date=this_rx[0], rx_name=this_rx[1],
                                         rx_dosage=this_rx[2], rx_sig=this_rx[3], rx_comments=this_rx[4])

            rx_num_+= 1

            new_rx.save()


        ############ MAKING VACCINES ############
        for f in range(0,len(vaccine_list)):
            this_vac = make_vac_record(f)
            new_vac = models.Vaccines(u_name=USER_NAME, vac_date=this_vac[0], vac_type=this_vac[1], vac_comment=this_vac[2])

            new_vac.save()

        ############ MAKING APPOINTMENTS ############
        appt_token = fakegen.random_int(min=0, max=5, step=1)
        for g in range(0,appt_token):
            this_appt = make_appointment()
            new_appt = models.Appointment(appointment_date=this_appt[0], u_name=USER_NAME, appointment_comments=this_appt[1])

            new_appt.save()


        ############ MAKING BILLS ############
        bill_token = fakegen.random_int(min=0, max=10, step=1)
        for h in range(0, bill_token):
            this_bill = make_bill()
            new_bill = models.Bills(u_name=USER_NAME, charge_date=this_bill[0], doc_charges=this_bill[1],
                                    medi_charges=this_bill[2], room_charges=this_bill[3], surgery_charges=this_bill[4],
                                    admission_days=this_bill[5], nursing_charges=this_bill[6], advance=this_bill[7],
                                    test_charges=this_bill[8], bill_amount=this_bill[9], pay_date=this_bill[10],
                                    pay_amount=this_bill[11],ins_copay=this_bill[12], balance=this_bill[13])

            new_bill.save()


if __name__ == '__main__':
    print('~~Patient Creation Script~~')
    num_of_pts = input('How many patients do you want to make?: ')
    populate(int(num_of_pts))
    print('PATIENT CREATION COMPLETE! Made ' + num_of_pts + ' Users!')