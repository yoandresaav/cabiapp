# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Placa, ReporteProductividad


@admin.register(Placa)
class PlacaAdmin(admin.ModelAdmin):
    list_display = ('id', 'placa')


@admin.register(ReporteProductividad)
class ReporteProductividadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'placa',
        'dia',
        'numero_viajes',
        'horas_conexion',
        'monto_facturado',
        'gasolina_dia',
        'kilometros_dia',
        'create',
        'update',
    )
    list_filter = ('placa', 'create', 'update')