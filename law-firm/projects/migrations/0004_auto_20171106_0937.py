# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-06 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20171105_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document',
            field=models.FileField(null=True, upload_to='', verbose_name='Document Upload'),
        ),
        migrations.AddField(
            model_name='documentmovement',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='case',
            name='type',
            field=models.CharField(choices=[('', '---------'), ('عمال', 'عمال'), ('جنائية', 'جنائية')], max_length=100, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.CharField(choices=[('', '---------'), ('محمكة', 'محمكة')], max_length=100, null=True, verbose_name='Type'),
        ),
    ]
