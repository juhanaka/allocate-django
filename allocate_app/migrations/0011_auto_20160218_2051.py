# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-18 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate_app', '0010_auto_20160126_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='pattern',
            field=models.CharField(default='(?!.*)', max_length=200),
        ),
    ]