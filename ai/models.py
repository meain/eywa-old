from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone

class Querry(models.Model):
    querry_term = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(default = timezone.now)

    def __unicode__(self):
        return self.querry_term
