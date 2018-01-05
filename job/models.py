from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Job(models.Model):
    jid = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    prog = models.IntegerField(blank=True, null=True)
    ver = models.IntegerField(blank=True, null=True)
    startdate = models.BigIntegerField(blank=True, null=True)
    enddate = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'job'


class JobParam(models.Model):
    jid = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    wid = models.CharField(max_length=50, blank=True, null=True)
    backup = models.CharField(max_length=5, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'job_param'

class JobHistory(models.Model):
    user = models.CharField(max_length=20, blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    action = models.CharField(max_length=10, blank=True, null=True)
    jid = models.IntegerField(blank=True, null=True)
    datetime = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'job_history'