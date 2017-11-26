# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-05 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20171105_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nationality',
            options={'ordering': ['display_order', 'nationality_en'], 'verbose_name_plural': 'Nationalities'},
        ),
        migrations.AlterField(
            model_name='case',
            name='client_role',
            field=models.CharField(choices=[('', '---------'), ('مدعي', 'مدعي')], max_length=100, null=True, verbose_name='Client Role'),
        ),
        migrations.AlterField(
            model_name='case',
            name='opponent_role',
            field=models.CharField(choices=[('', '---------'), ('مدعي', 'مدعي')], max_length=100, null=True, verbose_name='Opponent Role'),
        ),
        migrations.AlterField(
            model_name='case',
            name='type',
            field=models.CharField(choices=[('', '---------'), ('جنائية', 'جنائية')], max_length=100, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('', '---------'), ('جواز سفر', 'جواز سفر')], max_length=100, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='documentmovement',
            name='hard_copy',
            field=models.BooleanField(default=False, verbose_name='Hard Copy Received?'),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='lookup_type',
            field=models.CharField(choices=[('ORGANIZATION_TYPE', 'Organization Type'), ('CASE_TYPE', 'Case Type'), ('CONSULTATION_TYPE', 'Consultation Type'), ('PAPERWORK_TYPE', 'Paperwork Type'), ('DOCUMENT_TYPE', 'Document Type'), ('COURT_ROLE', 'Court Role')], db_index=True, max_length=30, null=True),
        ),
    ]
