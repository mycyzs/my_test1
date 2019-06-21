# -*- coding: utf-8 -*-

from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=30,null=True)
    is_success = models.BooleanField(default=False)
    text = models.TextField(null=True)
    when_created = models.CharField(max_length=50,null=True)


class Server(models.Model):
    host = models.ForeignKey(Host)