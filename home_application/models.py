# -*- coding: utf-8 -*-

from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=30, null=True)
    biz_name = models.CharField(max_length=30, null=True)
    script = models.TextField(null=True)
    max_num = models.CharField(max_length=30, null=True)
    create_time = models.DateTimeField(null=True)
    comment = models.TextField(null=True)


class Task(models.Model):
    task_name = models.CharField(max_length=30,null=True)
    host = models.CharField(max_length=30,null=True)
    task_type = models.CharField(max_length=30,null=True)
    create_time = models.DateTimeField(null=True)
    etra = models.CharField(max_length=120, null=True)
    tem = models.ForeignKey(Host, related_name="task", null=True)



