from django.contrib.auth.models import User
from django.db import models


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

