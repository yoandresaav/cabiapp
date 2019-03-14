import requests 
import logging

from django import forms
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
)

from django.contrib.auth import get_user_model

from .utility import get_client_ip



User = get_user_model()

class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        max_length=254,
        help_text='Requerido. Introduzca un correo válido'
    )
    

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserCreationWithEmailForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': ca,
            'remoteip': get_client_ip(self.request)
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        status = verify_rs.get("success", False)
        if not status:
            raise forms.ValidationError(
                ('Falló la validación del Captcha.'), code='invalid',
            )
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo {email} ya existe'.format(email=email)) 
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        # user.set_password(user.password) # set password properly before commit
        user.password = self.cleaned_data["password1"]
        user.is_active=False
        if commit:
            user.save()
        return user


class CabiappPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CabiappPasswordResetForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': ca,
            'remoteip': get_client_ip(self.request)
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        status = verify_rs.get("success", False)
        if not status:
            raise forms.ValidationError(
                ('Falló la validación del Captcha.'), code='invalid',
            )


    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        try:
            email_message.send()
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))