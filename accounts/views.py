from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .forms import RegisterForm, EditAccountForm

@login_required #verifica se o user está logado ou faz redirect para a pag login
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST': #se for post chama o formulário
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #salvar o usário
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user) #esta view óq realmente coloca o usuariona sessão
            return redirect('core:home')
    else:
        form = RegisterForm()#senão for post vem um fform vazio
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance = request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance = request.user) #form vazio

    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            context['sucess'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name,context)