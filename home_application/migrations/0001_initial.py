# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('biz_name', models.CharField(max_length=30, null=True)),
                ('script', models.TextField(null=True)),
                ('max_num', models.CharField(max_length=30, null=True)),
                ('create_time', models.DateTimeField(null=True)),
                ('comment', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=30, null=True)),
                ('host', models.CharField(max_length=30, null=True)),
                ('task_type', models.CharField(max_length=30, null=True)),
                ('create_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='task',
            field=models.ForeignKey(related_name='template', to='home_application.Task'),
        ),
    ]
