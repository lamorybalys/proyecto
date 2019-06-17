# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-04 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trabaexpe', '0001_initial'),
        ('constancias', '0002_auto_20140801_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cambio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(blank=True, max_length=255, null=True)),
                ('observacion', models.CharField(blank=True, max_length=255, null=True)),
                ('expediente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes')),
            ],
        ),
    ]
