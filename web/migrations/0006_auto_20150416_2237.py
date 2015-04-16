# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150416_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userskill',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='userskill',
            name='user',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='UserSkill',
        ),
    ]
