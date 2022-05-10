from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
import datetime


# Create your models here.

class Doctor(models.Model):
    Days = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    start_hour = models.TimeField(default=datetime.time(hour=0, minute=0, second=0, microsecond=0))
    end_hour = models.TimeField(default=datetime.time(hour=23, minute=0, second=0, microsecond=0))
    schedule = MultiSelectField(choices=Days, default=0)

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
    end_time = models.TimeField()
    description = models.TextField(null=True)
    is_canceled = models.BooleanField(default=False)

    def get_patient(self):
        return str(self.patient)
    
    def get_doctor(self):
        return str(self.doctor)

    def __str__(self):
        return 'Appointment: ' + str(self.doctor) + ', ' + str(self.patient) \
               + ', ' + str(self.date) + ', ' + str(self.start_time) + str(self.is_canceled)
