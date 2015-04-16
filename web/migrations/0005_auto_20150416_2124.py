# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150416_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
