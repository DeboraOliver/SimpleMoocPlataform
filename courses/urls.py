from django.urls import path

from . import views

app_name= 'courses'

urlpatterns = [
    path('cursos/', views.index, name = 'index'),
    path('cursos/<slug:slug>/', views.details, name = 'details'),
    path('cursos/<slug:slug>/inscricao/', views.enrollment, name='enrollment'),

]