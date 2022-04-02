import datetime
import time

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


class CreatePatientForm(forms.ModelForm):
	class Meta:
		model = Patient
		fields = ('doctor',)


class CreateDoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ()


class DateInput(forms.DateInput):
	input_type = 'date'


class TimeInput(forms.TimeInput):
	input_type = 'time'
	js = 'interval : 30'


HOUR_CHOICES = []

for x in range(0, 24):
	HOUR_CHOICES.append((datetime.time(hour=x),
						time.strftime("%I:%M %p", time.strptime('{:02d}:00'.format(x), "%H:%M"))))
	HOUR_CHOICES.append((datetime.time(hour=x, minute=30),
						time.strftime("%I:%M %p", time.strptime('{:02d}:30'.format(x), "%H:%M"))))


class CreateAppointmentForm(forms.ModelForm):
	date = forms.DateField(widget=DateInput)

	class Meta:
		model = Appointment
		fields = ('date', 'start_time')
		widgets = {'start_time': forms.Select(choices=HOUR_CHOICES)}
