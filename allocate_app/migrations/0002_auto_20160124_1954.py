# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('allocate_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecalendareventmodel',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='allocate_app.ProjectModel'),
        ),
    ]
