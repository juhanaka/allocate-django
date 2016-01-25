# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate_app', '0006_auto_20160125_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmodel',
            name='project_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='googlecalendareventmodel',
            name='event_id',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterUniqueTogether(
            name='googlecalendareventmodel',
            unique_together=set([('user', 'event_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectmodel',
            unique_together=set([('user', 'project_id')]),
        ),
    ]
