from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('PatientPortal', views.patientPortal, name='patientPortal'),
    path('DoctorPortal', views.doctorPortal, name='doctorPortal'),
    path("doctorPage/<username>", views.doctorPage, name="doctorPage"),
    path("patientMakeAppointment", views.patientMakeAppointment, name="patientMakeAppointment"),
    path("patientPage/<username>", views.patientPage, name="patientPage"),
    path("patientViewAppointment", views.patientViewAppointment, name="patientViewAppointment"),
    path("doctorViewAppointment", views.doctorViewAppointment, name="doctorViewAppointment"),
    path("doctorSetAvailability", views.doctorSetAvailability, name="doctorSetAvailability"),
    path("cancelAppointment/<username>/<appointmentId>", views.cancelAppointment, name="cancelAppointment"), 
    path("logout", views.logout, name="logout"),
]