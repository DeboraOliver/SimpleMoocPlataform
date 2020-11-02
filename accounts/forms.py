from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User #Vms trocar pelo noso customUser
from django.contrib.auth import get_user_model #para usar nosso accounts.models.User

User = get_user_model()

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError(
                'A confirmação de senha não está correta',
            )
        return password2




    #Não precisamos mais verificar a unique do email com o custom User
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists(): #primeiro importe o usuario
    #         raise forms.ValidationError('Já existe usuário com este E-mail')
    #     return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False) #false não salva o usuario antes de checar oe-mail
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta: #agora que  há uma customUser precisaremos disso
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

    #gera um formulário baseadoem todos os campos q o modelo tem
    class Meta:
        model = User
        #vms  agora listas os campos q podem ser alterados no model q o django dá
        fields = ['username', 'email', 'name']