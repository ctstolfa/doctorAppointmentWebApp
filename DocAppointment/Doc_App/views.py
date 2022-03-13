from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
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
            return render(request, 'patientPage.html', {'user': user})
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
            doctor = Doctor.objects.all().filter(user=user)
            patients = Patient.objects.all().filter(doctor=doctor[0])
            return render(request, 'doctorPage.html', {'user': user, 'patients': patients})
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


def doctorPage(request, username):
    # If no such user exists raise 404
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements in template
    editable = False
    # Handling non authenticated user for obvious reasons
    if request.user.is_authenticated and request.user == user:
        editable = True

    context = locals()
    template = 'doctorPage.html'
    return render(request, template, context)



def doctorPage(request, username):
    # If no such user exists raise 404
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements in template
    editable = False
    # Handling non authenticated user for obvious reasons
    if request.user.is_authenticated and request.user == user:
        editable = True

    context = locals()
    template = 'doctorPage.html'
    return render(request, template, context)
