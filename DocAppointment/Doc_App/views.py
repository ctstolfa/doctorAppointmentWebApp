from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user
from .models import Patient, Doctor


def home(request):
    return render(request, 'home.html', {})

def patientPortal(request):
    if request.method == 'POST':
        username = request.POST['username']
        password_su = request.POST.get('password_su')
        con_password = request.POST['con_password']
        doctor = request.POST['doctor']
        # user validation
        if Patient.object.filter(username=username):
            messages.error(request, "username already exist! please try some other user name")
            return redirect('home')
        if len(username) > 16:
            messages.error(request, "username must be under 16 charcters")
            return redirect('home')
        if con_password != password_su:
            messages.error(request, "passwords didn't match!")
        newPatient = Patient.object.create_user(username, password_su)
        newPatient.save()
        messages.success(request, "your account has been  successfully created")
        return redirect("home")
    return render(request, 'patientPortal.html', {})

def doctorPortal(request):
    return render(request, 'doctorPortal.html', {})

# Create your views here.
