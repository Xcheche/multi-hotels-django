from django.db import models


#Abstract class for common fields
class TimeStampedModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True