# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20161130_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
