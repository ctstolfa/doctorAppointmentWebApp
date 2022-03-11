from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Doctor


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
