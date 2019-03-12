from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
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
