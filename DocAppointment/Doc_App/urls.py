from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('PatientPortal', views.patientPortal, name='patientPortal'),
    path('DoctorPortal', views.doctorPortal, name='doctorPortal'),
]