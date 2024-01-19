from django.db import models
from authenticate.models import User
from helpers.models import trackingModel

class todoList(trackingModel):
    title = models.CharField(max_length= 100)
    description = models.TextField()
    isCompleted = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Create your models here.
