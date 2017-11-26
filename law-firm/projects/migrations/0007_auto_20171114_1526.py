# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-14 15:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20171109_0943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'verbose_name': 'Case', 'verbose_name_plural': 'Cases'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelOptions(
            name='consultation',
            options={'verbose_name': 'Consultation', 'verbose_name_plural': 'Consultations'},
        ),
        migrations.AlterModelOptions(
            name='court',
            options={'verbose_name': 'Court', 'verbose_name_plural': 'Courts'},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Employee', 'verbose_name_plural': 'Employees'},
        ),
        migrations.AlterModelOptions(
            name='lookup',
            options={'ordering': ['lookup_type', '-display_order'], 'verbose_name': 'Look up', 'verbose_name_plural': 'Look ups'},
        ),
        migrations.AlterModelOptions(
            name='nationality',
            options={'ordering': ['display_order', 'nationality_en'], 'verbose_name': 'Nationality', 'verbose_name_plural': 'Nationalities'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='paperwork',
            options={'verbose_name': 'Paperwork', 'verbose_name_plural': 'Paperwork Projects'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]
