# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='task',
            field=models.ForeignKey(related_name='template', to='home_application.Task', null=True),
        ),
    ]
