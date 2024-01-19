from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    isemailverified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
# Create your models here.
