import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cedus.settings')

import django
django.setup()

import decimal
import random
from patient.models import *
from faker import Faker

fakegen = Faker()


# returns a 2d-list of allergies and their severity
def gen_allergy(num_of_allergies):
    list_of_drugs = ['ampicillin', 'aztreonam', 'cefotaxime', 'ceftazidime', 'ceftriaxone', 'ciprofloxacin',
                     'clindamycin', 'co-trimoxazole', 'daptomycin', 'enviomycin', 'ethambutol', 'imipenem/cilastin',
                     'isoniazid', 'linezolid', 'meropenem', 'metronidazole', 'penicillin', 'quinidine', 'rifampicin',
                     'streptomycin', 'sulphadiamine', 'sulphadiazine', 'tobramycin', 'vancomycin', 'fluconazole',
                     'itraconazole', 'acycolvir', 'amprenavir', 'darunavir', 'efavirenz', 'enfuvartide', 'nelfinavir',
                     'nevirapine', 'tipranavir', 'zidovudine', 'adalimumab', 'cetuximab', 'glatiramer acetate',
                     'infliximab', 'l-asparaginase', 'carboplatin', 'cisplatin', 'cytarabine', 'docetaxel',
                     'imatinib mesylate',
                     'lenalidomide', 'mechlorethamine', '6-mercaptopurine', 'oxaliplatin', 'paclitaxel',
                     'sunitinib', 'thalidomide', 'azathioprine', 'cyclosporine', 'dapsone', 'hydroxychloroquine',
                     'mesalazine', 'methotrexate',
                     'mycophenolate mofetil', 'd-peniciliamine', 'sulfasalazine', 'carbamazepine', 'oxcarbazepine',
                     'phenobarbital', 'phenytoin', 'anastrazole', 'corticotropine', 'follicle-stimulating hormone',
                     'growth hormone',
                     'insulin', 'antithymocyte globulin', 'allopurinol', '5-aminosalicylic acid', 'buprenorphine',
                     'calcitonin',
                     'clopidrogel', 'colchicine', 'desferrioxamine', 'enoxaparine', 'erythropoietin',
                     'ferrous compounds', 'fluorercein', 'fluoxetine', 'furosemide', 'heparin', 'imiglucerase',
                     'interferon', 'isonicotinic acid hydrazine', 'methylphenidate', 'neuromuscular receptor',
                     'blockers', 'opioids', 'radiocontrast media', 'ubiquinone', 'warfarin']

    allergy_drug_list = []
    severity_list = []
    for i in range(0, num_of_allergies):
        random_int = fakegen.random_int(min=0, max=(len(list_of_drugs) - 1), step=1)
        allergy_drug_list.append(list_of_drugs[random_int])

        random_severity = fakegen.random_int(min=0, max=18, step=1)

        severity = ''
        if 0 <= random_severity <= 10:
            severity = 'low'
        elif 11 <= random_severity <= 15:
            severity = 'medium'
        else:
            severity = 'large'

        severity_list.append(severity)

    allergy_list = zip(allergy_drug_list, severity_list)
    return list(allergy_list)


def make_profile(number_of_profiles):
    # default user role, everyone generated will be a patient
    fk_user_role = User_Role(role_id=1, role='Patient')

    # loop to make profiles
    for a in range(0, number_of_profiles):
        # user id generation
        fk_id = fakegen.random_number(digits=8, fix_len=True)
        # user email generation
        fk_email = fakegen.email()
        # user password generation
        fk_password = fakegen.password(length=12)
        # user phonenumber generation
        fk_phone_num = fakegen.phone_number()

        # make user object
        fk_user = User_Cedus(user_id=fk_id, user_email=fk_email, user_password=fk_password,
                             phone_num=fk_phone_num, role_id=fk_user_role)
        # save object
        fk_user.save()

        # patient id generation
        fk_p_id = fakegen.random_number(digits=8, fix_len=True)

        # gender generation
        # 1 = male, 2 = female, 3 = other
        gen_gender = fakegen.random_int(min=1, max=3, step=1)
        fk_p_gender = ''
        fk_p_f_name = ''
        fk_p_l_name = ''
        # male
        if gen_gender == 1:
            fk_p_gender = 'M'
            fk_p_f_name = fakegen.first_name_male()
            fk_p_l_name = fakegen.last_name_male()
        # female
        elif gen_gender == 2:
            fk_p_gender = 'F'
            fk_p_f_name = fakegen.first_name_female()
            fk_p_l_name = fakegen.last_name_female()
        # other
        else:
            fk_p_gender = 'Ot'  # other
            fk_p_f_name = fakegen.first_name()
            fk_p_l_name = fakegen.last_name()

        # date of birth generation
        fk_p_dob = fakegen.date_of_birth(minimum_age=18, maximum_age=100)

        # city of residence generation
        fk_p_city = fakegen.city()
        # state of residence generation
        fk_p_state = fakegen.state_abbr()
        # zipcode of residence generation
        fk_p_zipcode = fakegen.postcode_in_state(fk_p_state)
        # language of patient generation
        fk_p_language = fakegen.language_name()

        # make patient object, link user object made from above
        fk_patient = Patient(p_id=fk_p_id, p_f_name=fk_p_f_name, p_l_name=fk_p_l_name,
                             p_dob=fk_p_dob, p_gender=fk_p_gender, p_city=fk_p_city,
                             p_state=fk_p_state, p_zipcode=fk_p_zipcode, p_language=fk_p_language, user_id=fk_user)

        # save patient object
        fk_patient.save()

        # determine number of allergies
        allergy_token = fakegen.random_int(min=0, max=15, step=1)
        num_of_allergy = 0
        if 0 <= allergy_token <= 9:
            num_of_allergy = 0
        elif 10 <= allergy_token <= 12:
            num_of_allergy = 1
        elif 13 <= allergy_token <= 14:
            num_of_allergy = 2
        else:
            num_of_allergy = 3

        # generate allergy and severity of allergy list
        fk_pt_allergy_list = gen_allergy(num_of_allergy)
        # iterate through list and save individual into db
        for b in fk_pt_allergy_list:
            # make object
            fk_allergy = Allergies(p_id=fk_patient, aller_to=b[0], aller_comments=b[1])
            fk_allergy.save()

        # generate vitals
        # generate number of vital readings
        vital_token = fakegen.random_int(min=5, max=20, step=1)
        for c in range(0, vital_token):
            # deciding blood group based on percentage of population
            fk_date = fakegen.date_between(start_date='-3y', end_date='today')
            fk_blood_grp = ''
            fk_sys = 0
            fk_dia = 0
            fk_wbc = 0
            fk_rbc = 0
            vt_comments = ''

            blood_grp_num = fakegen.random_int(min=0, max=99, step=1)
            if 0 <= blood_grp_num <= 35:
                blood_grp = 'O+'
            elif 36 <= blood_grp_num <= 65:
                blood_grp = 'A+'
            elif 66 <= blood_grp_num <= 78:
                blood_grp = 'O-'
            elif 78 <= blood_grp_num <= 86:
                blood_grp = 'A-'
            elif 87 <= blood_grp_num <= 94:
                blood_grp = 'B+'
            elif 95 <= blood_grp_num <= 96:
                blood_grp = 'B-'
            elif 97 <= blood_grp_num <= 98:
                blood_grp = 'AB+'
            else:
                blood_grp = 'AB-'

            # deciding blood pressure based on percentage of population
            b_pressure_type = fakegen.random_int(min=0, max=99, step=1)
            if 0 <= b_pressure_type <= 46:
                # hyper tension
                fk_sys = fakegen.random_int(min=130, max=200, step=1)
                fk_dia = fakegen.random_int(min=80, max=100, step=1)
            elif 47 <= b_pressure_type <= 96:
                # normal blood pressure
                fk_sys = fakegen.random_int(min=91, max=129, step=1)
                fk_dia = fakegen.random_int(min=61, max=79, step=1)
            else:
                # low blood pressure
                fk_sys = fakegen.random_int(min=70, max=90, step=1)
                fk_dia = fakegen.random_int(min=40, max=60, step=1)

            fk_wbc = fakegen.random_int(min=4500, max=11000, step=1)
            fk_rbc = decimal.Decimal(str(round(random.uniform(4.2, 6.1), 2)))

            # height in ft
            fk_height = decimal.Decimal(str(round(random.uniform(4.08, 6.50), 2)))
            # weight in lbs
            fk_weight = decimal.Decimal(str(round(random.uniform(100.00, 330.00), 2)))

            fk_vitals = Vitals(p_id=fk_patient, vt_date=fk_date, vt_bloodgroup=fk_blood_grp, vt_bp_sys=fk_sys,
                                vt_bp_dia=fk_dia, vt_wbc=fk_wbc, vt_rbc=fk_rbc, vt_height=fk_height,
                               vt_weight=fk_weight)

            fk_vitals.save()


if __name__ == '__main__':
    role_check = input('Populating Script!:\n Did you remember to run save_roles.py? (y/n)')
    if input == 'y':
        no = input('Number of Users you want to make: ')
        # number of users you want to make
        make_profile(int(no))
        print('Population Complete! Made ' + no + ' Users!')

    else:
        print('Please run save_roles.py!')
