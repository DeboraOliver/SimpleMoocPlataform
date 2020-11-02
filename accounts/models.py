import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,UserManager)

#AbstratcUser tras a logica de alterar senha e last login.
#O  permission tras a segurança do django

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'Nome de usuário só pode conter letras, digítos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank = True, default=False)
    date_joined = models.DateTimeField(
        'Data de entrada', auto_now_add=True
    ) #quando for salvo pela primeira vez

    objects = UserManager()
    #vms indicar os campos que serão unicos
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #para ser compativel com o django app usuario

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

