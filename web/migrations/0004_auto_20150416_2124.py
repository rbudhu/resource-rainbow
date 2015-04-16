# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150415_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 21, 24, 6, 41069)),
        ),
    ]
