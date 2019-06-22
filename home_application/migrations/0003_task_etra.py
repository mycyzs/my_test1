# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190622_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='etra',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
