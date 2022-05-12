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
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required


def home(request):
	return render(request, 'home.html', {})


def patientPortal(request):
    userForm = CreateUserForm()
    patientForm = CreatePatientForm()
    if request.method == "POST":
        userForm = CreateUserForm(request.POST)
        patientForm = CreatePatientForm(request.POST)
    if request.POST.get('submit') == 'Login':
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
    elif request.POST.get('submit') == 'Register':
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
    if request.POST.get('submit') == 'Login':
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
    elif request.POST.get('submit') == 'Register':
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


@login_required()
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

    patients = Patient.objects.all().filter(doctor=(Doctor.objects.get(user=user)))
    context = locals()
    template = 'doctorPage.html'
    return render(request, template, context)


@login_required()
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
    patient = Patient.objects.get(user=user)

    context = locals()
    template = 'patientPage.html'
    return render(request, template, context)


@login_required()
def patientMakeAppointment(request):
    appointment_form = CreateAppointmentForm()
    patient = Patient.objects.get(user=request.user)
    existing_apps = Appointment.objects.all().filter(doctor=patient.doctor).filter(is_canceled=False)\
        .order_by('date', 'start_time')
    if request.method == "POST":
        appointment_form = CreateAppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            time = appointment.start_time
            app_date = appointment.date
            existing_check = len(Appointment.objects.all()
                                 .filter(date=app_date).filter(start_time=time)
                                 .filter(doctor=patient.doctor).filter(is_canceled=False)) == 0
            time_check = patient.doctor.start_hour <= time < patient.doctor.end_hour
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
                return render(request, 'patientMakeAppointment.html',
                              {'appointment_form': appointment_form, 'patient': patient,
                               'doctor': patient.doctor, 'appointments': existing_apps})

    template = 'patientMakeAppointment.html'
    context = {'appointment_form': appointment_form, 'patient': patient,
               'doctor': patient.doctor, 'appointments': existing_apps}
    return render(request, template, context)


@login_required()
def patientViewAppointment(request):
    current_patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=current_patient).filter(is_canceled=False)\
        .order_by('date', 'start_time')
    canceledAppointments = Appointment.objects\
        .filter(patient=current_patient).filter(is_canceled=True).filter(canceled_by_doc=True)\
        .order_by('date', 'start_time')
    for a in appointments:
        if a.date < datetime.today().date():
            a.delete()
    context = locals()
    template = 'patientViewAppointment.html'
    return render(request, template, context)


@login_required()
def doctorViewAppointment(request):
    current_doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=current_doctor).filter(is_canceled=False)\
        .order_by('date', 'start_time')
    canceledAppointments = Appointment.objects\
        .filter(doctor=current_doctor).filter(is_canceled=True).filter(canceled_by_doc=False)\
        .order_by('date', 'start_time')
    for a in appointments:
        if a.date < datetime.today().date():
            a.delete()
    context = locals()
    template = 'doctorViewAppointment.html'
    return render(request, template, context)


@login_required()
def doctorSetAvailability(request):
    doctor = Doctor.objects.get(user=request.user)
    patients = Patient.objects.all().filter(doctor=doctor)
    availability_form = SetDoctorAvailability(instance=request.user.doctor)
    if request.method == "POST":
        availability_form = SetDoctorAvailability(request.POST, instance=request.user.doctor)
        if availability_form.is_valid():
            availability_form.save()
            appointments = Appointment.objects.filter(doctor=doctor)
            cancel_apps = []
            for a in appointments:
                if a.start_time < datetime.strptime(availability_form["start_hour"].value(), '%H:%M:%S').time() \
                        or a.end_time > datetime.strptime(availability_form["end_hour"].value(), '%H:%M:%S').time():
                    cancel_apps.append(a.id)
                elif not (str(a.date.weekday()) in list(doctor.schedule)):
                    cancel_apps.append(a.id)
            return redirect('scheduleCancelAppointment', appointments=cancel_apps)
    template = 'doctorSetAvailability.html'
    context = {'availability_form': availability_form}
    return render(request, template, context)


@login_required()
def cancelAppointment(request, appointmentId):
    appointment = Appointment.objects.get(id=appointmentId)
    appointment.is_canceled = True

    template = "patientViewAppointment.html"
    if len(Patient.objects.all().filter(user=request.user)) == 1:
        appointment.canceled_by_doc = False
        appointment.save()
        template = "patientViewAppointment.html"
        current_patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=current_patient).filter(is_canceled=False)\
            .order_by('date', 'start_time')
        canceledAppointments = Appointment.objects\
            .filter(patient=current_patient).filter(is_canceled=True).filter(canceled_by_doc=True)\
            .order_by('date', 'start_time')
        context = locals()
        return render(request, template, context)
        
    elif len(Doctor.objects.all().filter(user=request.user)) == 1:
        appointment.canceled_by_doc = True
        appointment.save()
        template = "doctorViewAppointment.html"
        current_doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=current_doctor).filter(is_canceled=False)\
            .order_by('date', 'start_time')
        canceledAppointments = Appointment.objects\
            .filter(doctor=current_doctor).filter(is_canceled=True).filter(canceled_by_doc=False)\
            .order_by('date', 'start_time')
        context = locals()
        return render(request, template, context)
        
    context = locals()
    return render(request, template, context)


@login_required()
def scheduleCancelAppointment(request, appointments):
    temp = appointments.replace('[', '').replace(']', '')
    apps = temp.split(',')
    for a in apps:
        try:
            appointment = Appointment.objects.get(id=int(a))
            appointment.is_canceled = True
            appointment.canceled_by_doc = True
            appointment.save()
        finally:
            apps = temp.split(',')

    patients = Patient.objects.all().filter(doctor=Doctor.objects.get(user=request.user))
    return render(request, 'doctorPage.html', {'user': request.user, 'patients': patients})


@login_required()
def acceptCanceledAppointment(request, appointmentId):
    appointment = Appointment.objects.get(id=appointmentId)
    appointment.delete()
    template = "patientViewAppointment.html"
    if len(Patient.objects.all().filter(user=request.user)) == 1:
        template = "patientViewAppointment.html"
        current_patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=current_patient).filter(is_canceled=False) \
            .order_by('date', 'start_time')
        canceledAppointments = Appointment.objects.filter(patient=current_patient)\
            .filter(is_canceled=True).filter(canceled_by_doc=True).order_by('date', 'start_time')
        context = locals()
        return render(request, template, context)

    elif len(Doctor.objects.all().filter(user=request.user)) == 1:
        template = "doctorViewAppointment.html"
        current_doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=current_doctor).filter(is_canceled=False) \
            .order_by('date', 'start_time')
        canceledAppointments = Appointment.objects.filter(doctor=current_doctor)\
            .filter(is_canceled=True).filter(canceled_by_doc=False).order_by('date', 'start_time')
        context = locals()
        return render(request, template, context)

    context = locals()
    return render(request, template, context)
    
@login_required()
def logout(request):
    logout_user(request)
    return redirect("home")
