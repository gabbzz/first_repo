# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-28 13:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20180728_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='fine',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='issue_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 28, 13, 9, 22, 937127)),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 4, 13, 9, 22, 937150)),
        ),
    ]
