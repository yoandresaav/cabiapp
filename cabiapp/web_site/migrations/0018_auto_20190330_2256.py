# Generated by Django 2.1.7 on 2019-03-30 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0017_reporteproductividad_fecha_reporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporteproductividad',
            name='fecha_reporte',
            field=models.DateField(verbose_name='Fecha que reporta'),
        ),
    ]
