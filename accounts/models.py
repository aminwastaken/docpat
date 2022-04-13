from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    DOCTOR = "doctor"
    PATIENT = "patient"
    USER_TYPES = [
        (DOCTOR, "Doctor"),
        (PATIENT, "Patient"),
    ]
    user_type = models.CharField(
        max_length=10, choices=USER_TYPES, default='user')
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.house_number + ' ' + self.street + ' ' + self.city + ' ' + self.country
