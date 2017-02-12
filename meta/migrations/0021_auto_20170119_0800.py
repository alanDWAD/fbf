# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-19 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0020_profile_id_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='house_occupancy_choice',
            field=models.CharField(choices=[(b'DL', b'Driving Licence'), (b'PP', b'Passport'), (b'NI', b'Mational ID')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
