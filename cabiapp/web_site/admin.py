# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Placa, ReporteProductividad


@admin.register(Placa)
class PlacaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'placa')
    list_filter = ('user',)


@admin.register(ReporteProductividad)
class ReporteProductividadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'placa',
        'dia',
        'numero_viajes',
        'total_facturado',
        'horas_conexion',
        'monto_facturado_cabify',
        'monto_facturado_didi',
        'monto_facturado_uber',
        'monto_facturado_beat',
        'gasolina_dia',
        'kilometros_dia',
        'create',
        'update',
    )
    list_filter = ('user', 'placa', 'create', 'update')