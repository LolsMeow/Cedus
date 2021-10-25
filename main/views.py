from django.shortcuts import render, redirect
from .forms import infoReg, PatientForm, register, updateInfo, userInfo
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
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
                return redirect('main:dashboard')

            else:
                messages.error(request, 'Invalid Username or Password')

        else:
            messages.error(request, 'Invalid Username or Password')

    form = AuthenticationForm()
    return render(request=request, template_name='main/login.html', context={'form': form})

def information_request(request):
    if not request.user.is_active:
        return redirect('main:register')
    if request.method == 'POST':
        p = Patient.objects.all().get(user=request.user)
        form = infoReg(data=request.POST, instance=p)
        p = form.save()
        return redirect('main:login')
    form = infoReg()
    return render(request=request, template_name='main/info.html', context={'information_form': form})

def auth_logout(request):
    logout(request)
    return redirect('main:dashboard')


def dashboard(request):
    if not request.user.is_active:
        return redirect('main:login')

    u = User.objects.get(username=request.user)
    p = Patient.objects.get(user=request.user)
    form = updateInfo(instance=p)
    userForm = userInfo(instance=u)

    if request.method == 'POST':
        u = User.objects.all().get(username=request.user)
        userForm = userInfo(data=request.POST, instance=u)
        p = Patient.objects.all().get(user=request.user)
        form = updateInfo(data=request.POST, instance=p)
        if form.is_valid() and userForm.is_valid():
            u = userForm.save()
            p = form.save()
        else:
            return render(request, 'main/dashboard.html', locals())
    return render(request, 'main/dashboard.html', locals())




