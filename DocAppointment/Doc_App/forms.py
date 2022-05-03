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
		widgets = {
			"doctor": forms.Select(attrs={"class": "select"}),
		}


class CreateDoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ()


class DateInput(forms.DateInput):
	input_type = 'date'


class TimeInput(forms.TimeInput):
	input_type = 'time'
	js = 'interval : 30'


class CreateAppointmentForm(forms.ModelForm):

	date = forms.DateField(widget=DateInput)

	class Meta:
		time_choices = []

		for x in range(0, 24):
			time_choices.append((datetime.time(hour=x),
								 time.strftime("%I:%M %p", time.strptime('{:02d}:00'.format(x), "%H:%M"))))
			time_choices.append((datetime.time(hour=x, minute=30),
								 time.strftime("%I:%M %p", time.strptime('{:02d}:30'.format(x), "%H:%M"))))

		model = Appointment
		fields = ('date', 'start_time', 'description')
		widgets = {'start_time': forms.Select(choices=time_choices)}


class SetDoctorAvailability(forms.ModelForm):
	class Meta:
		hour_choices = []

		for x in range(0, 24):
			hour_choices.append((datetime.time(hour=x),
								 time.strftime("%I:%M %p", time.strptime('{:02d}:00'.format(x), "%H:%M"))))

		model = Doctor
		fields = ('start_hour', 'end_hour', 'schedule')
		widgets = {'start_hour': forms.Select(choices=hour_choices), 'end_hour': forms.Select(choices=hour_choices)}