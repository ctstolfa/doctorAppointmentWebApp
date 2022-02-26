from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})

def patientPortal(request):
    return render(request, 'patientPortal.html', {})

def doctorPortal(request):
    return render(request, 'doctorPortal.html', {})

# Create your views here.
