from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, default='user')
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.username
