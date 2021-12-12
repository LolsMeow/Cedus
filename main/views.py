from django.shortcuts import render, redirect
from .forms import infoReg, PatientForm, register, updateInfo, userInfo, makeappointment, admin_register, Vital_Forms, Diag_Forms, Po_Forms, Prescription_Forms, Vaccine_Forms, Records_Forms, Appointments_Forms
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import *


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
            pay_ = Payment.objects.create(u_name=patient.user.username)
            pay_.save()
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
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    u = User.objects.get(username=request.user)
    userForm = userInfo(instance=u)
    p = Patient.objects.get(user=request.user)
    form = updateInfo(instance=p)

    if request.method == 'POST':

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
    else:
        form = Appointment.objects.all().filter(u_name=request.user)
        form = {'form': form}
        return render(request, 'main/appointments.html', form)
# def vitals_view_test(request, user_):
#     if request.method == 'GET':
#         vital_data = Vitals.objects.all().filter(u_name=user_)
#         form = {'vitalData': vital_data}
#         return render(request, 'main/vitals_test.html', form)

def vitals_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        form = Vitals.objects.all().filter(u_name=request.user)
        form = {'form': form}
        return render(request, 'main/vitals_test.html', form)

# def diag_view_test(request, user_):
#     if request.method == 'GET':
#         diag_data = Diagnosis.objects.all().filter(u_name=user_)
#         form = {'diagData': diag_data}
#         return render(request, 'main/diag_test.html', form)

def diag_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        diag_data = Diagnosis.objects.all().filter(u_name=request.user)
        form = {'diag_data': diag_data}
        return render(request, 'main/diag_test.html', form)

# def rx_view_test(request, user_):
#     if request.method == 'GET':
#         rx_data = Prescription.objects.all().filter(u_name=user_)
#         form = {'rxData': rx_data}
#         return render(request, 'main/rx_test.html', form)

def rx_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        pdata = Prescription.objects.all().filter(u_name=request.user)
        form = {'pdata': pdata}
        return render(request, 'main/rx_test.html', form)

# def phys_orders_view_test(request, user_):
#     if request.method == 'GET':
#         po_data = Phys_Orders.objects.all().filter(u_name=user_)
#         form = {'poData': po_data}
#         return render(request, 'main/po_test.html', form)

def phys_orders_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        physdata = Phys_Orders.objects.all().filter(u_name=request.user)
        form = {'physdata': physdata}
        return render(request, 'main/po_test.html', form)

# def vaccines_view_test(request, user_):
#     if request.method == 'GET':
#         vac_data = Vaccines.objects.all().filter(u_name=user_)
#         form = {'vaxData': vac_data}
#         return render(request, 'main/vax_test.html', form)

def vaccines_view(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    else:
        form = Vaccines.objects.all().filter(u_name=request.user)
        form = {'form': form}
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
    else:
        app_data = Appointment.objects.all().filter(u_name=request.user)
        bill_data = Bills.objects.all().filter(u_name=request.user)
        #pay_data = Payment.objects.all().filter(u_name=request.user)
        form = {'app_data': app_data, 'billData': bill_data}
        return render(request, 'main/records_test.html', form)


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
    return user.groups.filter(name='Staff').exists() or user.groups.filter(name='Pharmacist').exists() or user.groups.filter(name='Doctor').exists()


def add_items(request, model, form):

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.u_name = request.user
            info.save()
            print('working')
            if is_staff(request.user):
                if model == Vitals:
                    return redirect('main:admin_vitals')
                elif model == Diagnosis:
                    return redirect('main:admin_diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:admin_rx')
                elif model == Prescription:
                    return redirect('main:admin_phys')
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
                    return redirect('main:rx')
                elif model == Prescription:
                    return redirect('main:phys')
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
            print(is_staff(request.user))
            if is_staff(request.user):
                if model == Vitals:
                    return redirect('main:admin_vitals')
                elif model == Diagnosis:
                    return redirect('main:admin_diagnosis')
                elif model == Phys_Orders:
                    return redirect('main:admin_rx')
                elif model == Prescription:
                    return redirect('main:admin_phys')
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
                    return redirect('main:rx')
                elif model == Prescription:
                    return redirect('main:phys')
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


def delete_items(pk, model):

    model.objects.filter(id=pk).delete()

    if is_staff(request.user):
        if model == Vitals:
            return redirect('main:admin_vitals')
        elif model == Diagnosis:
            return redirect('main:admin_diagnosis')
        elif model == Phys_Orders:
            return redirect('main:admin_rx')
        elif model == Prescription:
            return redirect('main:admin_phys')
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
            return redirect('main:rx')
        elif model == Prescription:
            return redirect('main:phys')
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


def patient_search(request):
    if request.method == 'GET' and request.GET.get("search_box") != None:
        search_text = request.GET.get("search_box")
        request.session['user'] = search_text
        return redirect('main:admin_dashboard')
    else:
        return render(request, 'main/patient_search.html')

def admin_dashboard(request):
    # if not request.user.is_active or request.user.is_superuser:
    #     return redirect('main:login')
    user = request.session.get('user')
    u = User.objects.get(username=user)
    userForm = userInfo(instance=u)
    p = Patient.objects.get(user=u)
    form = updateInfo(instance=p)

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


def admin_makeappt(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
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
    else:
        user = request.session.get('user')
        form = Appointment.objects.all().filter(u_name=user)
        form = {'form': form}
        return render(request, 'main/admin_appointments.html', form)
# def vitals_view_test(request, user_):
#     if request.method == 'GET':
#         vital_data = Vitals.objects.all().filter(u_name=user_)
#         form = {'vitalData': vital_data}
#         return render(request, 'main/vitals_test.html', form)

def admin_vitals(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        user = request.session.get('user')
        form = Vitals.objects.all().filter(u_name=user)
        form = {'form': form}
        return render(request, 'main/admin_vitals.html', form)

# def diag_view_test(request, user_):
#     if request.method == 'GET':
#         diag_data = Diagnosis.objects.all().filter(u_name=user_)
#         form = {'diagData': diag_data}
#         return render(request, 'main/diag_test.html', form)

def admin_diagnosis(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        user = request.session.get('user')
        diag_data = Diagnosis.objects.all().filter(u_name=user)
        form = {'diag_data': diag_data}
        return render(request, 'main/admin_diag.html', form)

# def rx_view_test(request, user_):
#     if request.method == 'GET':
#         rx_data = Prescription.objects.all().filter(u_name=user_)
#         form = {'rxData': rx_data}
#         return render(request, 'main/rx_test.html', form)

def admin_rx(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        user = request.session.get('user')
        pdata = Prescription.objects.all().filter(u_name=user)
        form = {'pdata': pdata}
        return render(request, 'main/admin_rx.html', form)

# def phys_orders_view_test(request, user_):
#     if request.method == 'GET':
#         po_data = Phys_Orders.objects.all().filter(u_name=user_)
#         form = {'poData': po_data}
#         return render(request, 'main/po_test.html', form)

def admin_phys(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')

    else:
        user = request.session.get('user')
        physdata = Phys_Orders.objects.all().filter(u_name=user)
        form = {'physdata': physdata}
        return render(request, 'main/admin_po.html', form)

# def vaccines_view_test(request, user_):
#     if request.method == 'GET':
#         vac_data = Vaccines.objects.all().filter(u_name=user_)
#         form = {'vaxData': vac_data}
#         return render(request, 'main/vax_test.html', form)

def admin_vaccines(request):
    if not request.user.is_active or request.user.is_superuser:
        return redirect('main:login')
    else:
        user = request.session.get('user')
        form = Vaccines.objects.all().filter(u_name=user)
        form = {'form': form}
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
    else:
        user = request.session.get('user')
        app_data = Appointment.objects.all().filter(u_name=user)
        bill_data = Bills.objects.all().filter(u_name=user)
        #pay_data = Payment.objects.all().filter(u_name=request.user)
        form = {'app_data': app_data, 'billData': bill_data}
        return render(request, 'main/admin_records.html', form)
