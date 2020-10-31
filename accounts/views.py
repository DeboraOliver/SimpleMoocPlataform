from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.conf import settings

from .forms import RegisterForm

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST': #se for post chama o formulário
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #salvar o usário
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()#senão for post vem um fform vazio
    context = {
        'form': form
    }
    return render(request, template_name, context)