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

class EditAccountForm(forms.ModelForm):
    #EVITE REPETIÇÕES
    def clean_email(self):
        email = self.cleaned_data['email']
        #vms filtarr todos os usuario com esse emailMENOS o usuário atual. Assim verificamos se existe um usuário com este email
        queryset = User.obejcts.filter(
            email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este E-mail')
        return email

    #gera um formulário baseadoem todos os campos q o modelo tem
    class Meta:
        model = User
        #vms  agora listas os campos q podem ser alterados no model q o django dá
        fields = ['username', 'email', 'first_name', 'last_name']