import json

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import infoReg, PatientForm, register, updateInfo, userInfo, makeappointment, admin_register, Vital_Forms, \
    Diag_Forms, Po_Forms, Prescription_Forms, Vaccine_Forms, Records_Forms, Appointments_Forms
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import *
from .decorators import allowed_users
import requests

# =>SEARCH VIEWS STARTS HERE
# search method for Vitals
def search_vitals(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Vitals.objects.filter(
            u_name=request.user, vt_bloodgroup__icontains=search_str) | Vitals.objects.filter(u_name=request.user,
                                                                                              vt_date__icontains=search_str)
        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for Diagnosis
def search_diag(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Diagnosis.objects.filter(
            u_name=request.user, diagnosis_date__icontains=search_str) | Diagnosis.objects.filter(
            u_name=request.user, diagnosis_status__icontains=search_str)

        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for "Physician Orders"
def search_phyorders(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Phys_Orders.objects.filter(
            u_name=request.user, order_date__icontains=search_str) | Phys_Orders.objects.filter(
            u_name=request.user, order_contents__icontains=search_str)

        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for "Prescriptions"
def search_rx(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Prescription.objects.filter(
            u_name=request.user, rx_date__icontains=search_str) | Prescription.objects.filter(
            u_name=request.user, rx_name__icontains=search_str) | Prescription.objects.filter(
            u_name=request.user, rx_dosage__icontains=search_str) | Prescription.objects.filter(
            u_name=request.user, rx_sig__icontains=search_str)
        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for "Vaccine"
def search_vaccine(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Vaccines.objects.filter(
            u_name=request.user, vac_date__icontains=search_str) | Vaccines.objects.filter(
            u_name=request.user, vac_type__icontains=search_str)

        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for "Appointments"
def search_appointments(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        mydata = Appointment.objects.filter(
            u_name=request.user, appointment_date__icontains=search_str) | Appointment.objects.filter(
            u_name=request.user, appointment_comments__icontains=search_str)

        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# Search method for "Record(Bills)"

def search_billrecords(request):
    if request.method == 'POST':
        print('working')
        search_str = json.loads(request.body).get('searchText')
        mydata = Bills.objects.filter(
            u_name=request.user, id__icontains=search_str) | Bills.objects.filter(
            u_name=request.user, charge_date__icontains=search_str) | Bills.objects.filter(
            u_name=request.user, pay_date__icontains=search_str)

        data = mydata.values()
        return JsonResponse(list(data), safe=False)


# =>SEARCH VIEWS ENDS HERE


def admin_search_vitals(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Vitals.objects.filter(
                u_name=user, vt_bloodgroup__icontains=search_str) | Vitals.objects.filter(u_name=user,
                                                                                                  vt_date__icontains=search_str)
            data = mydata.values()
            return JsonResponse(list(data), safe=False)


# Search method for Diagnosis
def admin_search_diag(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Diagnosis.objects.filter(
                u_name=user, diagnosis_date__icontains=search_str) | Diagnosis.objects.filter(
                u_name=user, diagnosis_status__icontains=search_str)

            data = mydata.values()
            return JsonResponse(list(data), safe=False)


# Search method for "Physician Orders"
def admin_search_phyorders(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Phys_Orders.objects.filter(
                u_name=user, order_date__icontains=search_str) | Phys_Orders.objects.filter(
                u_name=user, order_contents__icontains=search_str)

            data = mydata.values()
            print(data)
            return JsonResponse(list(data), safe=False)


# Search method for "Prescriptions"
def admin_search_rx(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Prescription.objects.filter(
                u_name=user, rx_date__icontains=search_str) | Prescription.objects.filter(
                u_name=user, rx_name__icontains=search_str) | Prescription.objects.filter(
                u_name=user, rx_dosage__icontains=search_str) | Prescription.objects.filter(
                u_name=user, rx_sig__icontains=search_str)

            data = mydata.values()
            return JsonResponse(list(data), safe=False)


# Search method for "Vaccine"
def admin_search_vaccine(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Vaccines.objects.filter(
                u_name=user, vac_date__icontains=search_str) | Vaccines.objects.filter(
                u_name=user, vac_type__icontains=search_str)

            data = mydata.values()
            return JsonResponse(list(data), safe=False)


# Search method for "Appointments"
def admin_search_appointments(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Appointment.objects.filter(
                u_name=user, appointment_date__icontains=search_str) | Appointment.objects.filter(
                u_name=user, appointment_comments__icontains=search_str)

            data = mydata.values()
            return JsonResponse(list(data), safe=False)


# Search method for "Record(Bills)"

def admin_search_billrecords(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            mydata = Bills.objects.filter(
                u_name=user, id__icontains=search_str) | Bills.objects.filter(
                u_name=user, charge_date__icontains=search_str) | Bills.objects.filter(
                u_name=user, pay_date__icontains=search_str)

            data = mydata.values()
            return JsonResponse(list(data), safe=False)


def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = register(request.POST)
        patient_form = PatientForm(request.POST)
        if form.is_valid() and patient_form.is_valid():
            user = form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            group = Group.objects.get(name='Patient')
            user.groups.add(group)

            # create empty patient related objects
            ins = Insurance.objects.create(u_name=patient.user.username)
            ins.save()
            allg = Allergies.objects.create(u_name=patient.user.username)
            allg.save()
            vital = Vitals.objects.create(u_name=patient.user.username)
            vital.save()
            diag = Diagnosis.objects.create(u_name=patient.user.username)
            diag.save()
            p_o = Phys_Orders.objects.create(u_name=patient.user.username)
            p_o.save()
            rx_ = Prescription.objects.create(u_name=patient.user.username)
            rx_.save()
            vax = Vaccines.objects.create(u_name=patient.user.username)
            vax.save()
            billy = Bills.objects.create(u_name=patient.user.username)
            billy.save()
            #pay_ = Payment.objects.create(u_name=patient.user.username)
            #pay_.save()
            login(request, user)
            return redirect('main:information')
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request,
                      template_name="main/register.html",
                      context={'form': form, 'patient_form': patient_form})
    else:
        form = register()
        patient_form = PatientForm()
        return render(request=request,
                      template_name="main/register.html",
                      context={'form': form, 'patient_form': patient_form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if is_patient(user):
                    return redirect('main:dashboard')
                elif is_admin(user):
                    return redirect('main:admin_reg')
                else:
                    return redirect('main:patient_search')
            else:
                messages.error(request, 'Invalid Username or Password')

        else:
            messages.error(request, 'Invalid Username or Password')

    form = AuthenticationForm()
    return render(request=request, template_name='main/login.html', context={'form': form})


def information_request(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:register')
    elif is_staff(request.user):
        return redirect('main:patient_search')
    if request.method == 'POST':
        p = Patient.objects.all().get(user=request.user)
        form = infoReg(data=request.POST, instance=p)
        if form.is_valid():
            p = form.save()
            return redirect('main:login')
        else:
            return render(request=request, template_name='main/info.html', context={'information_form': form})
    form = infoReg()
    return render(request=request, template_name='main/info.html', context={'information_form': form})


def auth_logout(request):
    logout(request)
    return redirect('main:dashboard')


def dashboard(request):
    if is_staff(request.user):
        return redirect('main:patient_search')
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    u = User.objects.get(username=request.user)
    p = Patient.objects.get(user=request.user)
    data = Insurance.objects.filter(u_name=request.user)
    allergies_data = Allergies.objects.filter(u_name=request.user)
    context = {'data': data, 'allergies_data': allergies_data}
    form = updateInfo(instance=p)
    userForm = userInfo(instance=u)

    if request.method == 'POST':
        group = request.user.groups.all()[0].name
        print(group)
        if group == 'Patient':
            u = User.objects.all().get(username=request.user)
            userForm = userInfo(data=request.POST, instance=request.user)
            p = Patient.objects.all().get(user=request.user)
            form = updateInfo(data=request.POST, instance=p)
        if form.is_valid() and (userForm.is_valid()):
            u = userForm.save()
            p = form.save()
        else:
            return render(request, 'main/dashboard.html', locals())
    return render(request, 'main/dashboard.html', locals())


def make_appointments(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:
        if request.method == 'POST':
            form = makeappointment(data=request.POST)
            if form.is_valid():
                appt = form.save(commit=False)
                appt.u_name = request.user
                appt.save()
            else:
                return render(request, 'main/make_appointments.html', context={'appointment_form': form})
        form = makeappointment()
        return render(request, 'main/make_appointments.html', context={'appointment_form': form})


def appointments_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/appointments.html')
            else:
                print(fromdate)
                print(todate)
                result = Appointment.objects.filter(appointment_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/appointments.html', form)

        data = Appointment.objects.filter(u_name=request.user).order_by('id')
        page_nator = Paginator(data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': data, 'pag_obj': pag_obj}
        return render(request, 'main/appointments.html', form)
        # form = Appointment.objects.all().filter(u_name=request.user)
        # form = {'form': form}
        # return render(request, 'main/appointments.html', form)


# def vitals_view_test(request, user_):
#     if request.method == 'GET':
#         vital_data = Vitals.objects.all().filter(u_name=user_)
#         form = {'vitalData': vital_data}
#         return render(request, 'main/vitals_test.html', form)

def vitals_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:

        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/vitals_test.html')
            else:
                print(fromdate)
                print(todate)
                result = Vitals.objects.filter(vt_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/vitals_test.html', form)

        data = Vitals.objects.filter(u_name=request.user).order_by('id')
        page_nator = Paginator(data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': data, 'pag_obj': pag_obj}
        return render(request, 'main/vitals_test.html', form)


# def diag_view_test(request, user_):
#     if request.method == 'GET':
#         diag_data = Diagnosis.objects.all().filter(u_name=user_)
#         form = {'diagData': diag_data}
#         return render(request, 'main/diag_test.html', form)

def diag_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:

        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/diag_test.html')
            else:
                print('diagnosis date filter called')
                result = Diagnosis.objects.filter(diagnosis_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/diag_test.html', form)

        diag_data = Diagnosis.objects.all().filter(u_name=request.user)
        page_nator = Paginator(diag_data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'diag_data': diag_data, 'pag_obj': pag_obj}
        return render(request, 'main/diag_test.html', form)


# def rx_view_test(request, user_):
#     if request.method == 'GET':
#         rx_data = Prescription.objects.all().filter(u_name=user_)
#         form = {'rxData': rx_data}
#         return render(request, 'main/rx_test.html', form)

def rx_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:

        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/rx_test.html')
            else:
                print('Prescription date filter called')
                result = Prescription.objects.filter(rx_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/rx_test.html', form)

        pdata = Prescription.objects.all().filter(u_name=request.user)
        page_nator = Paginator(pdata, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'pdata': pdata, 'pag_obj': pag_obj}
        return render(request, 'main/rx_test.html', form)


# def phys_orders_view_test(request, user_):
#     if request.method == 'GET':
#         po_data = Phys_Orders.objects.all().filter(u_name=user_)
#         form = {'poData': po_data}
#         return render(request, 'main/po_test.html', form)

def phys_orders_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:

        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/po_test.html')
            else:
                print('physician date filter called')
                result = Phys_Orders.objects.filter(order_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/po_test.html', form)

        physdata = Phys_Orders.objects.all().filter(u_name=request.user)
        page_nator = Paginator(physdata, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'physdata': physdata, 'pag_obj': pag_obj}
        return render(request, 'main/po_test.html', form)


# def vaccines_view_test(request, user_):
#     if request.method == 'GET':
#         vac_data = Vaccines.objects.all().filter(u_name=user_)
#         form = {'vaxData': vac_data}
#         return render(request, 'main/vax_test.html', form)

def vaccines_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/vax_test.html')
            else:
                print('Vaccines date filter called')

                result = Vaccines.objects.filter(vac_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj': result}
                return render(request, 'main/vax_test.html', form)
        form = Vaccines.objects.all().filter(u_name=request.user)
        page_nator = Paginator(form, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': form, 'pag_obj': pag_obj}
        return render(request, 'main/vax_test.html', form)


# def records_view_test(request, user_):
#     if request.method == 'GET':
#         app_data = Appointment.objects.all().filter(u_name=user_)
#         bill_data = Bills.objects.all().filter(u_name=user_)
#         pay_data = Payment.objects.all().filter(u_name=user_)
#         form = {'appData': app_data, 'billData': bill_data, 'payData': pay_data}
#         return render(request, 'main/records_test.html', form)

def records_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_staff(request.user):
        return redirect('main:patient_search')
    else:
        # app_data = Appointment.objects.all().filter(u_name=request.user)
        if request.method == 'POST':
            fromdate = request.POST.get('billfromdate')
            todate = request.POST.get('billtodate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/records_test.html')
            else:
                pag_obj_bill = Bills.objects.filter(charge_date__range=[fromdate, todate], u_name=request.user)
                form = {'pag_obj_pay': pag_obj_bill}
                print(form)
                return render(request, 'main/records_test.html', form)

        bill_data = Bills.objects.all().filter(u_name=request.user)
        page_nator = Paginator(bill_data, 6)
        page_number = request.GET.get('page_pay')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'billData': bill_data, 'pag_obj_pay': pag_obj}
        return render(request, 'main/records_test.html', form)


def patient_search(request):
    if request.method == 'GET' and request.GET.get("search_box") != None:
        search_text = request.GET.get("search_box")
        if Patient.objects.filter(user__username=search_text).exists():
            request.session['user'] = search_text
            return redirect('main:admin_dashboard')
        else:
            messages.error(request, 'Patient does not exist')
            return render(request, 'main/patient_search.html')
    else:
        return render(request, 'main/patient_search.html')

def patient_search_failed(request):
    if request.method == 'GET' and request.GET.get("search_box") != None:
        search_text = request.GET.get("search_box")
        #if (search_text == '' or search_text == None:
        request.session['user'] = search_text
        return redirect('main:admin_dashboard')
    else:
        return render(request, 'main/patient_search_failed.html')

def admin_dashboard(request):
    if is_patient(request.user):
        return redirect('main:dashboard')
    # if not request.user.is_active or request.user.is_superuser:
    #     return redirect('main:login')
    user = request.session.get('user')
    try:
        u = User.objects.get(username=user)
        userForm = userInfo(instance=u)
        p = Patient.objects.get(user=u)
        form = updateInfo(instance=p)
        data = Insurance.objects.filter(u_name=user)
        allergies_data = Allergies.objects.filter(u_name=user)
        context = {'data': data, 'allergies_data': allergies_data}
        if request.method == 'POST':
            u = User.objects.all().get(username=user)
            userForm = userInfo(data=request.POST, instance=u)
            p = Patient.objects.all().get(user=u)
            form = updateInfo(data=request.POST, instance=p)
            if form.is_valid() and (userForm.is_valid()):
                u = userForm.save()
                p = form.save()
            else:
                return render(request, 'main/admin_dashboard.html', locals())
        return render(request, 'main/admin_dashboard.html', locals())
    except User.DoesNotExist:
        return patient_search_failed(request)


def admin_makeappt(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            form = makeappointment(data=request.POST)
            if form.is_valid():
                appt = form.save(commit=False)
                appt.u_name = user
                appt.save()
            else:
                return render(request, 'main/admin_make.html', context={'appointment_form': form})
        form = makeappointment()
        return render(request, 'main/admin_make.html', context={'appointment_form': form})


def admin_appt(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_appointments.html')
            else:
                print(fromdate)
                print(todate)
                result = Appointment.objects.filter(appointment_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_appointments.html', form)

        data = Appointment.objects.filter(u_name=user).order_by('id')
        page_nator = Paginator(data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': data, 'pag_obj': pag_obj}
        return render(request, 'main/admin_appointments.html', form)
        # form = Appointment.objects.all().filter(u_name=user)
        # form = {'form': form}
        # return render(request, 'main/admin_appointments.html', form)


# def vitals_view_test(request, user_):
#     if request.method == 'GET':
#         vital_data = Vitals.objects.all().filter(u_name=user_)
#         form = {'vitalData': vital_data}
#         return render(request, 'main/vitals_test.html', form)

def admin_vitals(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_vitals.html')
            else:
                result = Vitals.objects.filter(vt_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_vitals.html', form)

        data = Vitals.objects.filter(u_name=user).order_by('id')
        page_nator = Paginator(data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': data, 'pag_obj': pag_obj}
        return render(request, 'main/admin_vitals.html', form)


# def diag_view_test(request, user_):
#     if request.method == 'GET':
#         diag_data = Diagnosis.objects.all().filter(u_name=user_)
#         form = {'diagData': diag_data}
#         return render(request, 'main/diag_test.html', form)

def admin_diagnosis(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')

    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_diag.html')
            else:
                print('diagnosis date filter called')
                result = Diagnosis.objects.filter(diagnosis_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_diag.html', form)

        diag_data = Diagnosis.objects.all().filter(u_name=user)
        page_nator = Paginator(diag_data, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'diag_data': diag_data, 'pag_obj': pag_obj}
        return render(request, 'main/admin_diag.html', form)


# def rx_view_test(request, user_):
#     if request.method == 'GET':
#         rx_data = Prescription.objects.all().filter(u_name=user_)
#         form = {'rxData': rx_data}
#         return render(request, 'main/rx_test.html', form)

def admin_rx(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')

    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_rx.html')
            else:
                print('Prescription date filter called')
                result = Prescription.objects.filter(rx_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_rx.html', form)

        pdata = Prescription.objects.all().filter(u_name=user)
        page_nator = Paginator(pdata, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'pdata': pdata, 'pag_obj': pag_obj}
        return render(request, 'main/admin_rx.html', form)


# def phys_orders_view_test(request, user_):
#     if request.method == 'GET':
#         po_data = Phys_Orders.objects.all().filter(u_name=user_)
#         form = {'poData': po_data}
#         return render(request, 'main/po_test.html', form)

def admin_phys(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')

    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_po.html')
            else:
                print('physician date filter called')
                result = Phys_Orders.objects.filter(order_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_po.html', form)

        physdata = Phys_Orders.objects.all().filter(u_name=user)
        page_nator = Paginator(physdata, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'physdata': physdata, 'pag_obj': pag_obj}
        return render(request, 'main/admin_po.html', form)


# def vaccines_view_test(request, user_):
#     if request.method == 'GET':
#         vac_data = Vaccines.objects.all().filter(u_name=user_)
#         form = {'vaxData': vac_data}
#         return render(request, 'main/vax_test.html', form)

def admin_vaccines(request):
    if not request.user.is_active or request.user.is_superuser:

        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_vax.html')
            else:
                print('Vaccines date filter called')

                result = Vaccines.objects.filter(vac_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj': result}
                return render(request, 'main/admin_vax.html', form)
        form = Vaccines.objects.all().filter(u_name=user)
        page_nator = Paginator(form, 6)
        page_number = request.GET.get('page')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'form': form, 'pag_obj': pag_obj}
        return render(request, 'main/admin_vax.html', form)


# def records_view_test(request, user_):
#     if request.method == 'GET':
#         app_data = Appointment.objects.all().filter(u_name=user_)
#         bill_data = Bills.objects.all().filter(u_name=user_)
#         pay_data = Payment.objects.all().filter(u_name=user_)
#         form = {'appData': app_data, 'billData': bill_data, 'payData': pay_data}
#         return render(request, 'main/records_test.html', form)

def admin_records(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    elif is_patient(request.user):
        return redirect('main:dashboard')
    else:
        user = request.session.get('user')
        if request.method == 'POST':
            fromdate = request.POST.get('billfromdate')
            todate = request.POST.get('billtodate')
            if fromdate == '' or todate == '':
                messages.error(request, 'Dates can not be blank')
                return render(request, 'main/admin_records.html')
            else:
                pag_obj_bill = Bills.objects.filter(charge_date__range=[fromdate, todate], u_name=user)
                form = {'pag_obj_pay': pag_obj_bill}
                return render(request, 'main/admin_records.html', form)

        bill_data = Bills.objects.all().filter(u_name=user)
        page_nator = Paginator(bill_data, 6)
        page_number = request.GET.get('page_pay')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'billData': bill_data, 'pag_obj_pay': pag_obj}
        return render(request, 'main/admin_records.html', form)


@allowed_users(allowed_roles=['Patient', 'Staff'])
def Allergy_Edit(request, id):
    allergy_data = Allergies.objects.get(id=id)
    print("hello from edit allergy")
    context = {'allergy_data': allergy_data}
    if request.method == 'GET':
        return render(request, 'main/edit_allergies.html', context)
    if request.method == 'POST':

        aller_to = request.POST.get('drug')
        remarks = request.POST.get('severity')

        if not aller_to:
            messages.error(request, 'Field is Required')
            return render(request, 'edit_allergies.html')
        if not remarks:
            messages.error(request, 'Field is Required')
            return render(request, 'edit_allergies.html')
        allergy_data.aller_drug = aller_to
        allergy_data.aller_severity = remarks
        allergy_data.save()
        if is_staff(request.user):
            return redirect('main:admin_dashboard')
        messages.success(request, 'Record Updated Successfully')
        return redirect('main:dashboard')
    return HttpResponse('Patient and Staff are Allowed to Edit Data')


@allowed_users(allowed_roles=['Patient'])
def insurance_Edit(request, id):
    data = Insurance.objects.get(id=id)
    context = {'data': data}
    if request.method == 'GET':
        return render(request, 'main/edit_insurance.html', context)
    if request.method == 'POST':

        name = request.POST.get('name')
        plan = request.POST.get('plan')
        Rx_bin = request.POST.get('Rx_bin')
        Rx_pcn = request.POST.get('Rx_pcn')
        Rx_Group = request.POST.get('Rx_Group')
        coverage = request.POST.get('coverage')

        if not name:
            messages.error(request, 'Insurance Name is Required')
            return render(request, 'edit_insurance.html')
        if not plan:
            messages.error(request, 'Insurance Plan is Required')
            return render(request, 'edit_insurance.html')
        if not Rx_bin:
            messages.error(request, 'Rx_Bin is Required')
            return render(request, 'edit_insurance.html')
        if not Rx_pcn:
            messages.error(request, 'Rx_Pcn is Required')
            return render(request, 'edit_insurance.html')
        if not Rx_Group:
            messages.error(request, 'Rx_Group is Required')
            return render(request, 'edit_insurance.html')
        if not coverage:
            messages.error(request, 'Coverage is Required')
            return render(request, 'edit_insurance.html')
        data.ins_name = name
        data.ins_plan = plan
        data.ins_rx_bin = Rx_bin
        data.ins_rx_pcn = Rx_pcn
        data.ins_rx_group = Rx_Group
        data.ins_coverage = coverage
        data.save()
        messages.success(request, 'Record Updated Successfully')
        return redirect('main:dashboard')
    return HttpResponse('Access Granted to Patient Only')

def provider_details(request):

        if request.method == 'POST':

            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')

            request.session["firstname"] = firstname
            request.session["lastname"] = lastname

            if not firstname:
                messages.error(request, 'First Name is Required')
                return render(request, 'main/provider_details.html')
            if not lastname:
                messages.error(request, 'Last Name is Required')
                return render(request, 'main/provider_details.html')

        firstname = request.session.get('firstname', 'abc')
        lastname = request.session.get('lastname', 'abc')
        page_no = request.session.get('page_no')
        data = 'https://npiregistry.cms.hhs.gov/api/?number=&enumeration_type=&taxonomy_description=&first_name=' + firstname + '&use_first_name_alias=&last_name=' + lastname + '&organization_name=&address_purpose=&city=&state=&postal_code=&country_code=&limit=&skip=&version=2.1'

        response = requests.get(url=data).json()

        provider = []

        count = response['result_count']
        for item in range(count):
            provider.append({
                'NPI': '',
                'FirstName': '',
                'LastName': '',
                'Country': '',
                'Address': '',
                'City': '',
                'State': '',
                'Phone': '',
                'PostalCode': '',
                'Taxonomies': '',

            })

        for j, i in enumerate(response['results']):
            NPI = i['number']
            provider[j]['NPI'] = NPI
            FirstName = i['basic']['first_name']
            provider[j]['FirstName'] = FirstName
            LastName = i['basic']['last_name']
            provider[j]['LastName'] = LastName
            CountryName = i['addresses'][0]['country_name']
            provider[j]['Country'] = CountryName
            Address1 = i['addresses'][0]['address_1']
            provider[j]['Address'] = Address1
            city = i['addresses'][0]['city']
            provider[j]['City'] = city
            state = i['addresses'][0]['state']
            provider[j]['State'] = state
            telephone_number = i['addresses'][0]['telephone_number']
            provider[j]['phone'] = telephone_number
            postal_code = i['addresses'][0]['postal_code']
            provider[j]['postal_code'] = postal_code
            taxonomies = i['taxonomies'][0]['desc']
            provider[j]['taxonomies'] = taxonomies
            print(NPI, FirstName, LastName, Address1, telephone_number)

        page_no = request.GET.get('page_no')
        if not page_no:
            page_no = 5

        page_nator = Paginator(provider, page_no)
        page_number = request.GET.get('page')

        pag_obj = Paginator.get_page(page_nator, page_number)
        context = {'pag_obj': pag_obj}

        return render(request, 'main/provider_details.html', context)

        return render(request, 'main/provider_details.html')


@allowed_users(allowed_roles=['Patient', 'Staff'])
def appointments(request):
    if not request.user.is_active:
        return redirect('main:login')

    else:
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')

            result = Appointment.objects.filter(appointment_date__range=[fromdate, todate], u_name=request.user)
            form = {'pag_obj_pay': result}
            return render(request, 'main/appointments.html', form)
        form = Appointment.objects.all().filter(u_name=request.user)
        page_nator = Paginator(form, 5)
        page_number = request.GET.get('page_pay')
        pag_obj = Paginator.get_page(page_nator, page_number)
        form = {'pag_obj_pay': pag_obj}
        return render(request, 'main/appointments.html', form)


def admin_reg(request):
    if is_admin(request.user):
        if request.method == 'POST':
            print(request.POST)
            form = admin_register(request.POST)
            if form.is_valid():
                role = form.data.get('extra_field')
                user = form.save()
                if role == 'staff':
                    group = Group.objects.get(name='Staff')
                    user.groups.add(group)
                elif role == 'pharmacist':
                    group = Group.objects.get(name='Pharmacist')
                    user.groups.add(group)
                else:
                    group = Group.objects.get(name='Doctor')
                    user.groups.add(group)
                messages.error(request, "Successful registration.")
            return render(request=request,
                          template_name="main/admin_reg.html",
                          context={'form': form})
        else:
            form = admin_register()
            return render(request=request,
                          template_name="main/admin_reg.html",
                          context={'form': form})
    elif not request.user.is_active:
        return redirect('main:login')
    else:
        return redirect('main:dashboard')


def is_patient(user):
    return user.groups.filter(name='Patient').exists()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()


def is_pharmacist(user):
    return user.groups.filter(name='Pharmacist').exists()


def is_staff(user):
    return user.groups.filter(name='Staff').exists() or user.groups.filter(
        name='Pharmacist').exists() or user.groups.filter(name='Doctor').exists()


def add_items(request, model, form):

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            if is_staff(request.user):
                user = request.session.get('user')
                info.u_name = user
            else:
                info.u_name = request.user
            info.save()
            if is_staff(request.user):
                if model == Vitals:
                    return redirect('main:admin_vitals')
                elif model == Diagnosis:
                    return redirect('main:admin_diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:admin_phys')
                elif model == Prescription:
                    return redirect('main:admin_rx')
                elif model == Vaccines:
                    return redirect('main:admin_vaccines')
                elif model == Bills:
                    return redirect('main:admin_records')
                elif model == Appointment:
                    return redirect('main:admin_appt')
            else:
                if model == Vitals:
                    return redirect('main:vitals')
                elif model == Diagnosis:
                    return redirect('main:diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:phys')
                elif model == Prescription:
                    return redirect('main:rx')
                elif model == Vaccines:
                    return redirect('main:vaccines')
                elif model == Bills:
                    return redirect('main:records')
                elif model == Appointment:
                    return redirect('main:appt')
        else:
            return render(request, 'main/add.html', {'form': form})
    else:
        form = form()

        return render(request, 'main/add.html', {'form': form})


def add_vitals(request):
    return add_items(request, Vitals, Vital_Forms)


def add_diag(request):
    return add_items(request, Diagnosis, Diag_Forms)


def add_po(request):
    return add_items(request, Phys_Orders, Po_Forms)


def add_prescription(request):
    return add_items(request, Prescription, Prescription_Forms)


def add_vaccine(request):
    return add_items(request, Vaccines, Vaccine_Forms)


def add_records(request):
    return add_items(request, Bills, Records_Forms)


def add_appointments(request):
    return add_items(request, Appointment, Appointments_Forms)


def edit_items(request, pk, model, form):
    item = model.objects.all().get(pk=pk)

    if request.method == "POST":
        form = form(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if is_staff(request.user):
                if model == Vitals:
                    return redirect('main:admin_vitals')
                elif model == Diagnosis:
                    return redirect('main:admin_diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:admin_phys')
                elif model == Prescription:
                    return redirect('main:admin_rx')
                elif model == Vaccines:
                    return redirect('main:admin_vaccines')
                elif model == Bills:
                    return redirect('main:admin_records')
                elif model == Appointment:
                    return redirect('main:admin_appt')
            else:
                if model == Vitals:
                    return redirect('main:vitals')
                elif model == Diagnosis:
                    return redirect('main:diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:phys')
                elif model == Prescription:
                    return redirect('main:rx')
                elif model == Vaccines:
                    return redirect('main:vaccines')
                elif model == Bills:
                    return redirect('main:records')
                elif model == Appointment:
                    return redirect('main:appt')
    else:
        form = form(instance=item)

        return render(request, 'main/edit.html', {'form': form})


def edit_vitals(request, pk):
    return edit_items(request, pk, Vitals, Vital_Forms)


def edit_diag(request, pk):
    return edit_items(request, pk, Diagnosis, Diag_Forms)


def edit_po(request, pk):
    return edit_items(request, pk, Phys_Orders, Po_Forms)


def edit_prescription(request, pk):
    return edit_items(request, pk, Prescription, Prescription_Forms)


def edit_vaccine(request, pk):
    return edit_items(request, pk, Vaccines, Vaccine_Forms)


def edit_records(request, pk):
    return edit_items(request, pk, Bills, Records_Forms)


def edit_appointments(request, pk):
    return edit_items(request, pk, Appointment, Appointments_Forms)


def delete_items(request, pk, model):
    model.objects.filter(id=pk).delete()

    if is_staff(request.user):
        if model == Vitals:
            return redirect('main:admin_vitals')
        elif model == Diagnosis:
            return redirect('main:admin_diagnosis')
        elif model == Phys_Orders:
            return redirect('main:admin_phys')
        elif model == Prescription:
            return redirect('main:admin_rx')
        elif model == Vaccines:
            return redirect('main:admin_vaccines')
        elif model == Bills:
            return redirect('main:admin_records')
        elif model == Appointment:
            return redirect('main:admin_appt')
    else:
        if model == Vitals:
            return redirect('main:vitals')
        elif model == Diagnosis:
            return redirect('main:diagnosis')
        elif model == Phys_Orders:
            return redirect('main:phys')
        elif model == Prescription:
            return redirect('main:rx')
        elif model == Vaccines:
            return redirect('main:vaccines')
        elif model == Bills:
            return redirect('main:records')
        elif model == Appointment:
            return redirect('main:appt')


def delete_vitals(request, pk):
    return delete_items(request, pk, Vitals)


def delete_diag(request, pk):
    return delete_items(request, pk, Diagnosis)


def delete_po(request, pk):
    return delete_items(request, pk, Phys_Orders)


def delete_prescription(request, pk):
    return delete_items(request, pk, Prescription)


def delete_vaccine(request, pk):
    return delete_items(request, pk, Vaccines)


def delete_records(request, pk):
    return delete_items(request, pk, Bills)


def delete_appointments(request, pk):
    return delete_items(request, pk, Appointment)



