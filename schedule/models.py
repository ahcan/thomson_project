from __future__ import unicode_literals
import time
from django.db import models
from accounts.models import AuthUser

# Create your models here.
class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    create_time = models.IntegerField(blank=True, null=True)
    schedule_time = models.IntegerField(blank=True, null=True)
    action = models.PositiveSmallIntegerField()
    message = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)