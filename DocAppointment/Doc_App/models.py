from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

class Patient(models.Model):
    acc = models.ForeignKey(Account, on_delete=models.CASCADE)
    # doctor?


class Doctor(models.Model):
    acc = models.ForeignKey(Account, on_delete=models.CASCADE)
    # list of patients?
