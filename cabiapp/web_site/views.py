from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string

from django.contrib import messages

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import get_user_model, login

from .models import ReporteProductividad
from .forms import UserCreationWithEmailForm
from .tokens import account_activation_token

User = get_user_model()

class ReporteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'web_site/home.html'
    model = ReporteProductividad
    success_url = 'thanks/'
    fields = (
        'placa', 'dia', 'numero_viajes', 'horas_conexion', 'monto_facturado', 
        'gasolina_dia', 'kilometros_dia'
    )

class CreateAccountsView(CreateView):
    template_name = 'registration/create_accounts.html'
    form_class = UserCreationWithEmailForm

    def post(self, request, *args, **kwargs):
        form = UserCreationWithEmailForm(request.POST)
        if form.is_valid():

            # no save the user
            user = form.save()

            # create new user
            if user is not None:
                current_site = get_current_site(request)
                subject = 'Activando tu cuenta en CabiFleet'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                # Enviar correo de que  se creo el usuario
                user.email_user(subject, message)
                messages.success(request, 'Te hemos enviado un correo con el link de activación de tu cuenta')
                return HttpResponseRedirect(reverse_lazy('web_site:thanks_page'))

        return render(request, self.template_name, {'form':form})

    def get_success_url(self):
        # Go to login page
        return reverse('web_site:createreporte_page')

class ThanksView(LoginRequiredMixin, TemplateView):
    template_name = 'web_site/end.html'


class SuperAdminView(LoginRequiredMixin, ListView):
    template_name = 'web_site/super_admin.html'
    model = ReporteProductividad


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='cabiapp.backends.EmailOrUsernameModelBackend',)
        return redirect('web_site:createreporte_page')
    else:
        return render(request, 'registration/account_activation_invalid.html')