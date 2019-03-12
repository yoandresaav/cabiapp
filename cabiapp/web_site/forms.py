from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        max_length=254,
        help_text='Requerido. Introduzca un correo válido'
    )
    

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        # user.set_password(user.password) # set password properly before commit
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user
