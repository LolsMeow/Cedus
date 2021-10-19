from django.shortcuts import render
#import models from patients
from patient import views
# Create your views here.
from django.http import HttpResponse
from patient.models import *
import json


def get_info(request, find_user_id):
    if request.method == 'GET':
        try:
            ser_user = User_Cedus.objects.get(user_id=find_user_id)
            ser_patient = Patient.objects.get(user_id=ser_user)

            first_name = ser_patient.p_f_name
            last_name = ser_patient.p_l_name
            id_number = ser_patient.p_id

            result = {'Patient First Name:': first_name, 'Patient Last Name: ': last_name, 'Patient ID No: ':
                id_number}

            response = json.dumps(result)

        except:
            response = json.dumps([{'Error: No patient with that ID'}])

    return HttpResponse(response,content_type='text/json')


def profile(request, find_user_id):
    if request.method == 'GET':
        ser_user = User_Cedus.objects.get(user_id=find_user_id)
        ser_patient = Patient.objects.get(user_id=ser_user)
        first_name = ser_patient.p_f_name
        last_name = ser_patient.p_l_name
        id_number = ser_patient.p_id
        gender = ser_patient.p_gender
        dob = ser_patient.p_dob
        address = str(ser_patient.p_city+', '+ser_patient.p_state+', '+str(ser_patient.p_zipcode))

        line_1 = {'Patient Name: ': first_name + ' ' + last_name}
        line_2 = {'Patient ID No: ': str(id_number)}
        line_3 = {'Patient Gender: ': gender, 'Patient DOB: ': str(dob)}
        line_4 = {'Patient Address: ': address}

        response_line_1 = json.dumps(line_1)
        response_line_2 = json.dumps(line_2)
        response_line_3 = json.dumps(line_3)
        response_line_4 = json.dumps(line_4)

        return HttpResponse(response_line_1+'<br/>'+response_line_2+'<br/>'+response_line_3+'<br/>'+response_line_4)





