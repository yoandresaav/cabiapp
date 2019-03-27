from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    numero_viajes = models.PositiveIntegerField('Cantidad de Viajes Totales del Día', default=0)
    horas_conexion = models.PositiveIntegerField('Horas de Conexión', default=0)

    monto_facturado_cabify = models.PositiveIntegerField('Facturación Cabify (sin bonos, sin decimales)', default=0)
    monto_facturado_didi = models.PositiveIntegerField('Facturación Didi (sin bonos, sin decimales)', default=0)
    monto_facturado_uber = models.PositiveIntegerField('Facturación Uber (sin bonos, sin decimales)', default=0)
    monto_facturado_beat = models.PositiveIntegerField('Facturación Beat (sin bonos, sin decimales)', default=0)

    total_facturado = models.PositiveIntegerField('Total', default=0)

    gasolina_dia = models.PositiveIntegerField('Monto de Gasolina del día', default=0)
    kilometros_dia = models.PositiveIntegerField('Kilometros recorridos del día', default=0)

    create = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'ReportesProductividades'
        ordering = ('create',)

    def __str__(self):
        return '{0} + {1}'.format(self.placa, self.dia)
    

@receiver(post_save, sender=ReporteProductividad)
def save_reporte_productividad(sender, instance, created, **kwargs):
    total = (
        instance.monto_facturado_beat + instance.monto_facturado_cabify + instance.monto_facturado_didi + instance.monto_facturado_uber
    )
    if instance.total_facturado != total:
        instance.total_facturado = total
        instance.save()
    print('Total facturado {0}'.format(instance.total_facturado))
    