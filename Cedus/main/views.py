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


def dashboard(request):
    if not request.user.is_active:
        return redirect('main:login')
    p = Patient.objects.get(id=1)
    form = updateInfo(instance = p)
    if request.method == 'POST':
        p = Patient.objects.all().get(email=request.user)
        form = updateInfo(data=request.POST, instance=p)
        print(form)
        p = form.save()
    return render(request, 'main/dashboard.html', {'form':form})


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


