from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ReporteProductividad

class ReporteCreateView(CreateView):
    template_name = 'web_site/home.html'
    model = ReporteProductividad
    success_url = 'thanks/'
    fields = (
        'placa', 'dia', 'numero_viajes', 'horas_conexion', 'monto_facturado', 
        'gasolina_dia', 'kilometros_dia'
    )


class ThanksView(TemplateView):
    template_name = 'web_site/end.html'


class SuperAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'web_site/super_admin.html'
