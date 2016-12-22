# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20161219_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
        migrations.AddField(
            model_name='profile',
            name='verify_key',
            field=models.CharField(blank=True, max_length=250, verbose_name='key'),
        ),
    ]