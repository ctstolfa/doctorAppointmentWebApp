from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    doctor = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.user)


class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # list of patients?
