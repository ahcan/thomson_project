from __future__ import unicode_literals
import time
from django.db import models
#from accounts.models import AuthUser
from django.contrib.auth.models import User

# Create your models here.
class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    create_time = models.IntegerField(blank=True, null=True)
    schedule_time = models.IntegerField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    host = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)