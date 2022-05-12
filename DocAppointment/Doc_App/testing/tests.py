from django.test import TestCase
from ..models import Doctor
from ..models import Patient
from ..models import Appointment
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
# Create your tests here.


class DoctorModelTests(TestCase):
    def setUp(self):
        self.doc1 = Doctor.objects.create(user="doctor1")
        self.doc2 = Doctor.objects.create(user="doctor2")
        self.patient1 = Patient.objects.create(doctor=Doctor.objects.filter(user="doctor1"), user="patient1")
        self.patient2 = Patient.objects.create(doctor=Doctor.objects.filter(user="doctor2"), user="patient2")

class PatientModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='TestingThisPassword1@')
        self.user2 = User.objects.create_user(username='user2', password='TestingThisPassword2@')
        self.user3 = User.objects.create_user(username='user3', password='TestingThisPassword3@')
        self.user4 = User.objects.create_user(username='user4', password='TestingThisPassword4@')
        self.doc3 = Doctor.objects.create(user=User.objects.get(id=1))
        self.doc4 = Doctor.objects.create(user=User.objects.get(id=2))
        self.patient3 = Patient.objects.create(doctor=Doctor.objects.get(id=1), user=User.objects.get(id=3))
        self.patient4 = Patient.objects.create(doctor=Doctor.objects.get(id=2), user=User.objects.get(id=4))

    def test_patient_doctor(self):
        self.assertTrue(self.patient3 in list(Patient.objects.filter(doctor=self.doc3)))
        self.assertFalse(self.patient3 in list(Patient.objects.filter(doctor=self.doc4)))
        self.assertTrue(self.patient4 in list(Patient.objects.filter(doctor=self.doc4)))
        self.assertFalse(self.patient4 in list(Patient.objects.filter(doctor=self.doc3)))

    def test_add_patient_to_doctor(self):
        self.user5 = User.objects.create_user(username='user5', password='TestingThisPassword5@')
        self.patient5 = Patient.objects.create(doctor=Doctor.objects.get(id=1), user=User.objects.get(id=5))
        self.assertTrue(self.patient5 in list(Patient.objects.filter(doctor=self.doc3)))

class AppointmentModelTests(TestCase):
    def setUp(self):
        #self.patient6 = Patient.objects.create(doctor=Doctor.objects.filter(user="doctor2"), user="patient6")
        self.appointment1 = Appointment.objects.create(patient="patient1", doctor="doctor1", )
