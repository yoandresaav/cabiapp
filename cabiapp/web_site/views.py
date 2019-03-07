from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import ReporteProductividad

class ReporteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'web_site/home.html'
    model = ReporteProductividad
    success_url = 'thanks/'
    fields = (
        'placa', 'dia', 'numero_viajes', 'horas_conexion', 'monto_facturado', 
        'gasolina_dia', 'kilometros_dia'
    )

class CreateAccountsView(CreateView):
    template_name = 'web_site/accounts/create_accounts.html'
    form_class = UserCreationForm

    def get_success_url(self):
        # Go to login page
        return reverse('web_site:createreporte_page')

class ThanksView(TemplateView):
    template_name = 'web_site/end.html'


class SuperAdminView(LoginRequiredMixin, ListView):
    template_name = 'web_site/super_admin.html'
    model = ReporteProductividad
