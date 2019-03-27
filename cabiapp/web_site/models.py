from django.db import models
from django.contrib.auth import get_user_model

class Placa(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    placa = models.CharField('Placa que reportas', max_length=6)

    def __str__(self):
        return self.placa

class ReporteProductividad(models.Model):
    lunes = 'lun'
    martes = 'mar'
    miercoles = 'mie'
    jueves = 'jue'
    viernes = 'vie'
    sabado = 'sab'
    domingo = 'dom'

    DIAS_REPORTE = (
        (lunes,'Lunes'),
        (martes,'Martes'),
        (miercoles, 'Miércoles'),
        (jueves, 'Jueves'),
        (viernes, 'Viernes'),
        (sabado, 'Sabado'),
        (domingo, 'Domingo'),
    )

    user = models.ForeignKey(
        get_user_model(),
        related_name='reportes',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    placa = models.ForeignKey(Placa, on_delete=models.SET_NULL, null=True)
    dia = models.CharField('Día que reporta', max_length=10, choices=DIAS_REPORTE)

    numero_viajes = models.PositiveIntegerField('Cantidad de Viajes')
    horas_conexion = models.PositiveIntegerField('Horas de Conexión')

    monto_facturado = models.PositiveIntegerField('Monto Facturado')

    gasolina_dia = models.PositiveIntegerField('Monto de Gasolina del día', default=0)
    kilometros_dia = models.PositiveIntegerField('Kilometros recorridos del día', default=0)

    create = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'ReportesProductividades'
        ordering = ('create',)

    def __str__(self):
        return '{0} + {1}'.format(self.placa, self.dia) 
    
    