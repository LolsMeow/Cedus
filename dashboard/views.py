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

            result = {'Patient First Name: ': first_name, 'Patient Last Name: ': last_name, 'Patient ID No: ': id_number}

            response = json.dumps(result)

        except:
            response = json.dumps([{'Error: No patient with that ID'}])

    return HttpResponse(response,content_type='text/json')