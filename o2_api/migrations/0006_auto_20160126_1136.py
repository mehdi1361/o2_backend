# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 11:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('o2_api', '0005_auto_20160126_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='User_Game',
        ),
    ]
