from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from django.contrib import messages


from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail

from .models import ReporteProductividad
from .forms import UserCreationWithEmailForm, CabiappPasswordResetForm
from .tokens import account_activation_token

User = get_user_model()


def create_secure_uid(pk: str):
    try:
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except:
        return urlsafe_base64_encode(force_bytes(pk))


class ReporteCreateView(LoginRequiredMixin, CreateView):
    # Page report after login
    template_name = 'web_site/home.html'
    model = ReporteProductividad
    success_url = 'thanks/'


    fields = (
        'placa', 'fecha_reporte', 'numero_viajes', 'horas_conexion',
        'cobros_efectivo', 'monto_facturado_cabify', 'monto_facturado_didi', 
        'monto_facturado_uber', 'monto_facturado_beat', 'gasolina_dia', 'kilometros_dia'
    )

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        # send mail
        asunto = 'Nuevo reporte de {0}'.format(user)
        mensaje = 'Usuario: {0}\n'.format(user)
        if hasattr(self.object, 'fecha_reporte'): 
            mensaje += 'Dia del reporte: {0}\n'.format(self.object.fecha_reporte.strftime("%A"))
            mensaje += 'fecha_reporte: {0}\n'.format(self.object.fecha_reporte.strftime("%d-%m-%Y"))
        if hasattr(self.object, 'placa'):
            mensaje += 'Placa: {0}\n'.format(self.object.placa)
        if hasattr(self.object, 'numero_viajes'):
            mensaje += 'Viajes: {0}\n'.format(self.object.numero_viajes)
        if hasattr(self.object, 'horas_conexion'):
            mensaje += 'Horas: {0}\n'.format(self.object.horas_conexion)
        if hasattr(self.object, 'cobros_efectivo'):
            mensaje += 'Cobros en Efectivo: {0}\n'.format(self.object.cobros_efectivo)
        if hasattr(self.object, 'total_facturado'):
            mensaje += 'Total facturado: {0}\n'.format(self.object.total_facturado)

        send_mail(
            asunto,
            mensaje,
            'sitio@cabifleet.com',
            ['info@cabifleet.com'],
            fail_silently=False,
        )



        return super().form_valid(form)

class CreateAccountsView(CreateView):
    template_name = 'registration/create_accounts.html'
    form_class = UserCreationWithEmailForm

    def post(self, request, *args, **kwargs):
        form = UserCreationWithEmailForm(request.POST, request=request)
        if form.is_valid():

            # no save the user
            user = form.save()

            # create new user
            if user is not None:
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'uid': create_secure_uid(user.pk),
                    'token': account_activation_token.make_token(user),
                    'domain':get_current_site(request).domain,
                })
                messages.success(request, 'Ahora puedes entrar con tu usuario y contraseña')
                # Enviar correo de que  se creo el usuario
                """
                subject = 'Activando tu cuenta en CabiFleet'
                try:
                    user.email_user(subject, message)
                except Exception as e:
                    messages.error(request, 'Lo sentimos no hemos podido enviar un link de activación. Comunicate con nosotros.')
                    logging.getLogger("error_logger").error(repr(e))
                """
                return HttpResponseRedirect(reverse_lazy('web_site:thanks_page'))

        return render(request, self.template_name, {'form':form})

    def get_success_url(self):
        # Go to login page
        return reverse('web_site:createreporte_page')


class CheckViewReport(LoginRequiredMixin, TemplateView):
    template_name = ''


class ThanksView(LoginRequiredMixin, TemplateView):
    template_name = 'web_site/end.html'


class SuperAdminView(LoginRequiredMixin, ListView):
    # Admin. Ver todos los reportes
    template_name = 'web_site/admin_all_report.html'
    queryset = ReporteProductividad.objects.select_related(
        'placa', 'user'
    ).all()

class SuperVerUsers(LoginRequiredMixin, ListView):
    template_name = 'web_site/admin_all_user.html'
    queryset = User.objects.all().order_by('-last_login', '-date_joined')


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

class CabiAppPasswordResetView(PasswordResetView):
    form_class = CabiappPasswordResetForm
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        form = self.get_form()
        """
        form = CabiappPasswordResetForm(request.POST, request=request)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class VerMisReportesView(LoginRequiredMixin, ListView):
    # Ver mis reportes
    template_name = 'web_site/ver_mis_reportes.html'
    # model = ReporteProductividad
    
    def get_queryset(self):
        from .tasks import send_feedback_email_task
        try:
            send_feedback_email_task.delay("yoandre@gmail.com", "Hola mundo celery")
        except Exception as error:
            print('Error al enviar el correo: {0}'.format(error))

        user = self.request.user
        return user.reportes.select_related(
            'placa'
        ).all()

def username_check(request):
    if not request.method == 'POST' and request.is_ajax():
        raise Exception('Bad request')
    
    username = request.POST.get('username', '')
    if not username:
        raise Exception('No send username')
    
    u = User.objects.filter(username=username).first()
    return JsonResponse({'exists': u != None})
