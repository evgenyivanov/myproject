# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-09 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0016_auto_20170306_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='server',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
