# Generated by Django 2.1.7 on 2019-03-30 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0016_auto_20190329_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporteproductividad',
            name='fecha_reporte',
            field=models.DateField(default=datetime.date.today, verbose_name='Fecha que reporta'),
        ),
    ]
