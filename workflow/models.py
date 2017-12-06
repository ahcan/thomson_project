from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Workflow(models.Model):
    wid = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    pubver = models.IntegerField(blank=True, null=True)
    priver = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'workflow'