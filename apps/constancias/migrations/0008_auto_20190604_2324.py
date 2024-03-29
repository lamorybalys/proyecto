# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-05 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constancias', '0007_auto_20190604_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='segu_social',
            name='estatus',
            field=models.CharField(blank=True, choices=[('Pendiente', 'Pendiente'), ('Procesando', 'Procesando'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')], default='Pendiente', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='segu_social',
            name='const_1402',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='segu_social',
            name='const_1403',
            field=models.BooleanField(default=False),
        ),
    ]
