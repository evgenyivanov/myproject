# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-08 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20170208_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='checks_per_hour',
            field=models.FloatField(default=1.0),
        ),
    ]