# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20171127_1332'),
        ('accounting', '0009_auto_20171128_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='projects.Client'),
        ),
    ]
