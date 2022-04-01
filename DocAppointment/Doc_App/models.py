from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user)

    def get_doc(self):
        return str(self.doctor)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = start_time + timedelta(minutes = 30)


    def get_patient(self):
        return str(self.patient)
    
    def get_doctor(self):
        return str(self.doctor)

    

