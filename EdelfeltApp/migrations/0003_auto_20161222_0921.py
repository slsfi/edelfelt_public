# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EdelfeltApp', '0002_person_hide_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='language',
            field=models.CharField(max_length=100),
        ),
    ]
