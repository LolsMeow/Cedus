import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cedus.settings')

import django

django.setup()

import random

from patient.models import *

from faker import Faker

fakegen = Faker()


def make_profile(number_of_profiles):
    fk_user_role = User_Role(role_id=1, role='Patient')

    for i in range(0, number_of_profiles):
        fk_id = fakegen.random_number(digits=8, fix_len=True)
        fk_email = fakegen.email()
        fk_password = fakegen.password(length=12)
        fk_phone_num = fakegen.phone_number()

        fk_user = User_Cedus(user_id=fk_id, user_email=fk_email, user_password=fk_password,
                             phone_num=fk_phone_num, role_id=fk_user_role)
        fk_user.save()


        fk_p_id = fakegen.random_number(digits=8, fix_len=True)
        # 1 = male, 2 = female, 3 = other
        gen_gender = fakegen.random_int(1, 3, 1)
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

        fk_p_dob = fakegen.date_of_birth(minimum_age=18, maximum_age=100)

        fk_p_city = fakegen.city()
        fk_p_state = fakegen.state_abbr()
        fk_p_zipcode = fakegen.postcode_in_state(fk_p_state)
        fk_p_language = fakegen.language_name()

        fk_patient = Patient(p_id=fk_p_id, p_f_name=fk_p_f_name, p_l_name=fk_p_l_name,
                             p_dob=fk_p_dob, p_gender=fk_p_gender, p_city=fk_p_city,
                             p_state=fk_p_state, p_zipcode=fk_p_zipcode, p_language=fk_p_language, user_id=fk_user)

        fk_patient.save()


if __name__ == '__main__':
    print('Populating Script!')
    # number of users you want to make
    no = input('Number of Users you want to make: ')
    make_profile(int(no))
    print('Population Complete! Made' + no + 'Users!')
