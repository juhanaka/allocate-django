# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate_app', '0005_auto_20160124_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecalendareventmodel',
            name='event_id',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
