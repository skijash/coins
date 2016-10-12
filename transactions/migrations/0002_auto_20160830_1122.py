# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='timestamp',
            new_name='created_ts',
        ),
        migrations.AddField(
            model_name='transaction',
            name='started_ts',
            field=models.DateTimeField(null=True),
        ),
    ]
