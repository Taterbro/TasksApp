from django.db import models

class trackingModel(models.Model):
        createdAt = models.DateTimeField(auto_now=True) #every time an instance of this model is created, auto now sets the time at that time
        updatedAt = models.DateTimeField(auto_now_add=True) #same thing, but adds the time when it's updated as well

        class Meta:
                abstract = True
                ordering = ('-createdAt',) #orders it by date created in descending order, thus the minus sign