from django.urls import path

from . import views

app_name= 'courses'

urlpatterns = [
    path('cursos/', views.index, name = 'index'),
    path('cursos/<slug:slug>/', views.details, name = 'details'),
    path('cursos/<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
    path('cursos/<slug:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'),
    path('cursos/<slug:slug>/anuncios/', views.announcements, name='announcements'),
    path('cursos/<slug:slug>/anuncios/<int:pk>', views.show_announcement, name='show_announcement'),

]