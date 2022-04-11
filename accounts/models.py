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
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.username
