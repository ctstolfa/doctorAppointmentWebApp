from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Patient, Doctor
from .forms import CreateUserForm, CreatePatientForm, CreateDoctorForm


def home(request):
	return render(request, 'home.html', {})


def patientPortal(request):
    userForm = CreateUserForm()
    patientForm = CreatePatientForm()
    if request.method == "POST":
        userForm = CreateUserForm(request.POST)
        patientForm = CreatePatientForm(request.POST)
    if request.POST.get('submit') == 'login':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "home.html")
        else:
            messages.error(request, 'This Username Or Password does not exist')
            return redirect('patientPortal')
    elif request.POST.get('submit') == 'register':
        if userForm.is_valid() and patientForm.is_valid():
            userForm.save()
            patient = patientForm.save(commit=False)
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            patient.user = user
            patient.save()
            messages.success(request, "Registration successful!")
            return redirect('patientPortal')

    return render(request, 'patientPortal.html', {'user_form': userForm, 'patient_form': patientForm})


def doctorPortal(request):
    userForm = CreateUserForm()
    doctorForm = CreateDoctorForm()
    if request.method == "POST":
        userForm = CreateUserForm(request.POST)
        doctorForm = CreateDoctorForm(request.POST)
    if request.POST.get('submit') == 'login':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "home.html")
        else:
            messages.error(request, 'This Username Or Password does not exist')
            return redirect('doctorPortal')
    elif request.POST.get('submit') == 'register':
        if userForm.is_valid() and doctorForm.is_valid():
            userForm.save()
            doctor = doctorForm.save(commit=False)
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            doctor.user = user
            doctor.save()
            messages.success(request, "Registration successful!")
            return redirect('doctorPortal')

    return render(request, 'doctorPortal.html', {'user_form': userForm, 'patient_form': doctorForm})

# Create your views here.
