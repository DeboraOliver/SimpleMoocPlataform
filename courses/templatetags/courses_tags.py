from django.template import Library

register = Library() #vamos registrar nossas tags

from courses.models import Enrollment

#converte a função em uma tag q recebe e renderiza um template
#use em templates complexos e em templates que não serão reutilizados
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    #primeiro pegar a inscrição do usuario
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments': enrollments
    }
    return context

#esta tag atualiza o contexto, dou mais flexibilidade ao meu uso, do q a anterior
@register.simple_tag #assigment_tag não funciona mais
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)