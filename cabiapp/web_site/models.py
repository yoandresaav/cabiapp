from django.db import models

# Create your models here.

class Placa(models.Model):
    placa = models.CharField('Placa', max_length=6)

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

    def __str__(self):
        return '{0} + {1}'.format(self.placa, self.dia) 
    
    