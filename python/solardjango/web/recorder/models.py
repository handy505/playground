from django.db import models
from django.utils import timezone

# Create your models here.

class Record(models.Model):
    deviceid        = models.IntegerField()
    logged_datetime = models.DateTimeField()
    ac_output_power = models.IntegerField(default=0)

    def __str__(self):
        return '{}, {}, {}'.format(self.deviceid,
                                   self.logged_datetime, 
                                   self.ac_output_power)
