# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_task_etra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='tem',
            field=models.ForeignKey(related_name='task', to='home_application.Host', null=True),
        ),
    ]
