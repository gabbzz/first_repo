# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-29 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20180728_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='issue_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='return_date',
            field=models.DateTimeField(),
        ),
    ]