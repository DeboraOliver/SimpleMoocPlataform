from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name= 'core'

urlpatterns = [
    path('home/', views.home, name = 'home'),
	path('contato/', views.contact, name = 'contact'),
    path('', RedirectView.as_view(url='/home/'))
]