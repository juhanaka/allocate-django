# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 07:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0006_outlookcredentialsmodel_rescuetimetokenmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('employees', models.ManyToManyField(related_name='employee_of', to=settings.AUTH_USER_MODEL)),
                ('managers', models.ManyToManyField(related_name='manager_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
