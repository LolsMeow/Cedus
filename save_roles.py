import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cedus.settings')

import django

django.setup()

from patient.models import *

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
README!!!!
Remember to run save_roles.py before this script!
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def make_roles():
    #Class 1 User: Front end user.
    patient_role = User_Role(role_id=1, role='Patient')
    patient_role.save()
    print(str(patient_role.role_id)+' '+str(patient_role.role))

    #Class 2 Staff: Staff account intended to be used by nurses, technicians, and front-desk staff.
    staff_role = User_Role(role_id=2, role='Staff')
    staff_role.save()
    print(str(staff_role.role_id) + ' ' + str(staff_role.role))

    #Class 3 Pharmacist: Provider account for Pharmacists.
    pharmacist_role = User_Role(role_id=3, role='Pharmacist')
    pharmacist_role.save()
    print(str(pharmacist_role.role_id) + ' ' + str(pharmacist_role.role))

    #Class 4 Doctor: Provider account for Doctors and PA’s.
    doctor_role = User_Role(role_id=4, role='Doctor')
    doctor_role.save()
    print(str(doctor_role.role_id) + ' ' + str(doctor_role.role))

    #Class 5 Admin: Accounts intended to be used by managers and admin staff.
    #Iintended to create Class 2, 3, and 4 accounts
    admin_role = User_Role(role_id=5, role='Admin')
    admin_role.save()
    print(str(admin_role.role_id) + ' ' + str(admin_role.role))

    #Class 6 Client: The main account under which the app is based.
    #All other classes of users are made in relation to this.
    #There is only one main client account.
    #If a client requires more Admin accounts, they may create more Class 5 users.
    client_role = User_Role(role_id=6, role='Client')
    client_role.save()
    print(str(client_role.role_id) + ' ' + str(client_role.role))

if __name__ == '__main__':
    print('Roles Saving!')
    make_roles()
    print('All Roles Saved!')
