from django.urls import path

from . import views

urlpatterns = [
    path('cursos/', views.index, name = 'index'),
    path('cursos/<slug:slug>/', views.details, name = 'details'),
]