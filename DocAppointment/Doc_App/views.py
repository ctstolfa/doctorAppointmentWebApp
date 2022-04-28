from datetime import datetime, date, timedelta
#from readline import append_history_file

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Appointment, Patient, Doctor
from .forms import CreateUserForm, CreatePatientForm, CreateDoctorForm, CreateAppointmentForm, SetDoctorAvailability


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
            patient = Patient.objects.all().filter(user=user)
            if len(patient) == 0:
                messages.error(request, 'You are not a Patient')
                print('test')
                return redirect('patientPortal')
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
            doctor = Doctor.objects.filter(user=user)
            if len(doctor) == 0:
                messages.error(request, 'You are not a Doctor')
                return redirect('doctorPortal')
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


def patientPage(request, username):
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
    template = 'patientPage.html'
    return render(request, template, context)


def patientMakeAppointment(request):
    appointment_form = CreateAppointmentForm()
    if request.method == "POST":
        appointment_form = CreateAppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            time = appointment.start_time
            app_date = appointment.date
            patient = Patient.objects.get(user=request.user)
            existing_check = len(Appointment.objects.all()
                                 .filter(date=app_date).filter(start_time=time).filter(doctor=patient.doctor)) == 0
            time_check = patient.doctor.start_hour < time < patient.doctor.end_hour
            day_check = str(app_date.weekday()) in list(patient.doctor.schedule)
            future_check = app_date > datetime.today().date()
            if existing_check and time_check and day_check and future_check:
                appointment.patient = patient
                appointment.doctor = patient.doctor
                print(appointment.date.weekday())
                appointment.end_time = (datetime.combine(date.today(),
                                                         appointment.start_time) + timedelta(minutes=30)).time()
                appointment.save()
                return redirect('patientPage', username=request.user.username)
            else:
                if not existing_check:
                    messages.error(request, 'This appointment is not available')
                elif not time_check:
                    messages.error(request, 'The time selected is not during doctor hours')
                elif not day_check:
                    messages.error(request, 'The doctor does not work on this day')
                elif not future_check:
                    messages.error(request, 'This appointment is in the past')
                appointment_form = CreateAppointmentForm()
                return render(request, 'patientMakeAppointment.html', {'appointment_form': appointment_form})

    template = 'patientMakeAppointment.html'
    context = {'appointment_form': appointment_form}
    return render(request, template, context)


def patientViewAppointment(request):
    current_patient = Patient.objects.get(user=request.user)
    patientAppointments = Appointment.objects.filter(patient=current_patient)
    for a in patientAppointments:
        if a.date < datetime.today().date():
            a.delete()
    context = locals()
    template = 'patientViewAppointment.html'
    return render(request, template, context)


def doctorViewAppointment(request):
    current_doctor = Doctor.objects.get(user=request.user)
    doctorAppointments = Appointment.objects.filter(doctor=current_doctor)
    for a in doctorAppointments:
        if a.date < datetime.today().date():
            a.delete()
    context = locals()
    template = 'doctorViewAppointment.html'
    return render(request, template, context)


def doctorSetAvailability(request):
    doctor = Doctor.objects.get(user=request.user)
    patients = Patient.objects.all().filter(doctor=doctor)
    availability_form = SetDoctorAvailability(instance=request.user.doctor)
    if request.method == "POST":
        availability_form = SetDoctorAvailability(request.POST, instance=request.user.doctor)
        if availability_form.is_valid():
            availability_form.save()
            appointments = Appointment.objects.filter(doctor=doctor)
            for a in appointments:
                if a.start_time < doctor.start_hour or a.end_time > doctor.end_hour:
                    a.delete()
                elif not (str(a.date.weekday()) in list(doctor.schedule)):
                    a.delete()
            return render(request, 'doctorPage.html', {'user': request.user, 'patients': patients})
    template = 'doctorSetAvailability.html'
    context = {'availability_form': availability_form}
    return render(request, template, context)


