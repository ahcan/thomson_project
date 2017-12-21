from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Node(models.Model):
    nid = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    cpu = models.IntegerField(blank=True, null=True)
    alloccpu = models.IntegerField(blank=True, null=True)
    mem = models.IntegerField(blank=True, null=True)
    allocmem = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    uncreachable = models.CharField(max_length=5, blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'node'

class NodeDetail(models.Model):
    nid = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=20, blank=True, null=True)
    jid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'node_detail'