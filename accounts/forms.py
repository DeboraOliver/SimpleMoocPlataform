from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): #primeiro importe o usuario
            raise forms.ValidationError('Já existe usuário com este E-mail')
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False) #false não salva o usuario antes de checar oe-mail
        user.email = self.cleaned_data['email'] #tras apenas emails validos
        if commit:
            user.save()
        return user