# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='querry',
            name='querry_result',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
