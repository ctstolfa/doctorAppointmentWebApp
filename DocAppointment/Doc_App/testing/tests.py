import datetime

from django.test import TestCase
from ..models import Doctor, Patient, Appointment
from django.contrib.auth.models import User


class DoctorModelTests(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='TestingThisPassword1@')
		self.doc1 = Doctor.objects.create(user=User.objects.get(id=1))

	def test_doctor_creation(self):
		self.assertEquals(self.doc1.user, self.user1)
		self.assertEquals(self.doc1.start_hour, datetime.time(hour=0, minute=0, second=0, microsecond=0))
		self.assertEquals(self.doc1.end_hour, datetime.time(hour=23, minute=0, second=0, microsecond=0))
		self.assertEquals(self.doc1.schedule, '0')


class PatientModelTests(TestCase): #Lukas
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
		self.user1 = User.objects.create_user(username='user1', password='TestingThisPassword1@')
		self.user2 = User.objects.create_user(username='user2', password='TestingThisPassword2@')
		self.doctor = Doctor.objects.create(user=User.objects.get(id=1))
		self.patient = Patient.objects.create(doctor=Doctor.objects.get(id=1), user=User.objects.get(id=2))
		self.appointment = Appointment.objects.create(
			patient=Patient.objects.get(id=1),
			doctor=Doctor.objects.get(id=1),
			date=datetime.datetime(2022, 1, 1, 0, 0, 0, 0),
			start_time=datetime.time(hour=10, minute=0, second=0, microsecond=0),
			end_time=datetime.time(hour=10, minute=30, second=0, microsecond=0),
		)

	def test_appointment_creation(self):
		self.assertEqual(self.appointment.patient, self.patient)
		self.assertEqual(self.appointment.doctor, self.doctor)
		self.assertEqual(self.appointment.date, datetime.datetime(2022, 1, 1, 0, 0, 0, 0))
		self.assertEqual(self.appointment.start_time, datetime.time(hour=10, minute=0, second=0, microsecond=0))
		self.assertEqual(self.appointment.end_time, datetime.time(hour=10, minute=30, second=0, microsecond=0))

	def test_appointment_delete(self):
		self.appointment.delete()
		self.assertEqual(len(Appointment.objects.all()), 0)
