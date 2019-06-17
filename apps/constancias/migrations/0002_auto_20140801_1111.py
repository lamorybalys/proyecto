# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2014-08-01 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constancias', '0001_initial'),
        ('trabaexpe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segu_social',
            name='expediente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
        migrations.AddField(
            model_name='periodo',
            name='expediente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
        migrations.AddField(
            model_name='jubilacion',
            name='expediente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
        migrations.AddField(
            model_name='descan_trimes',
            name='expediente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
        migrations.AddField(
            model_name='cronologico',
            name='expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trabaexpe.Expedientes'),
        ),
    ]
