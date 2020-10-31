from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('entrar/', LoginView.as_view(
         template_name ='accounts/login.html'), name='login'),
    path('sair/', LogoutView.as_view(
         next_page='home'), name='logout'),
    path('cadastre-se', views.register, name='register')
]

