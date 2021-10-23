from django.shortcuts import render, redirect
from .forms import register, infoReg, updateInfo
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import *


def register_request(request):
    if request.method == "POST":
        form = register(request.POST)

        if form.is_valid():
            user = form.save()
            Patient.objects.create(first_name=user.first_name, last_name=user.last_name,
                                   name=user.first_name + ' ' + user.last_name, email=user.email,
                                   password=user.password)
            group = Group.objects.get(name='Patient')
            user.groups.add(group)
            login(request, user)
            return redirect('main:information')
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = register()
    return render(request=request, template_name="main/register.html", context={'register_form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main:dashboard')

            else:
                messages.error(request, 'Invalid Username or Password')

        else:
            messages.error(request, 'Invalid Username or Password')

    form = AuthenticationForm()
    return render(request=request, template_name='main/login.html', context={'form': form})


def auth_logout(request):
    logout(request)
    return redirect('main:dashboard')


def dashboard_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    p = Patient.objects.get(u_name=user)
    form = updateInfo(instance=p)
    if request.method == 'POST':
        p = Patient.objects.all().get(u_name=user)
        form = updateInfo(data=request.POST, instance=p)
        p = form.save()
    return render(request, 'main/dashboard_pt.html', {'form': form})


def dashboard_staff(request):
    if not request.user.is_active:
        return redirect('main:login')
    s = Staff.objects.get(u_name=user)
    form = updateInfo(instance=s)
    if request.method == 'POST':
        s = Staff.objects.all().get(u_name=user)
        form = updateInfo(data=request.POST, instance=s)
        s = form.save()
    return render(request, 'main/dashboard_staff.html', {'form': form})


def vitals_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        vital_data = Vitals.objects.all().filter(u_name=user)
        vital_entry = {'vitalData': vital_data}
    return render(request, 'main/vitals_test.html', vital_entry)


def diagnosis_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        diag_data = Diagnosis.objects.all().filter(u_name=user)
        diag_entry = {'diagData': diag_data}
    return render(request, 'main/diagnosis_test.html', diag_entry)


def phys_orders_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        phys_orders_data = Phys_Orders.objects.all().filter(u_name=user)
        phys_orders_entry = {'physOrders': phys_orders_data}
    return render(request, 'main/phys_orders_test.html', phys_orders_entry)


def prescription_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        rx_data = Prescription.objects.all().filter(u_name=user)
        rx_entry = {'rxData': rx_data}
    return render(request, 'main/prescription_test.html', rx_entry)


def vaccinations_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        vac_data = Vaccines.objects.all().filter(u_name=user)
        vac_entry = {'vaccine': vac_data}
    return render(request, 'main/vaccine_test.html', vac_entry)

def records_pt(request):
    if not request.user.is_active:
        return redirect('main:login')
    if request.method == 'POST':
        surgery_data = Surgeries.objects.all().filter(u_name=user)
        bill_data = Bills.objects.all().filter(u_name=user)
        payment_data = Payment.objects.all().filter(u_name=user)

        records_entry = {'surgeryData': surgery_data, 'billData': bill_data, 'payData': payment_data}
    return render(request, 'main/records_test.html', records_entry)

def information_request(request):
    if not request.user.is_active:
        return redirect('main:register')
    if request.method == 'POST':
        p = Patient.objects.all().get(email=request.user)
        form = infoReg(data=request.POST, instance=p)
        p = form.save()
        return redirect('main:login')
    form = infoReg()
    return render(request=request, template_name='main/info.html', context={'information_form': form})
