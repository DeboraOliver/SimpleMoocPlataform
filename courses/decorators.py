from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

def enrollment_required(view_func): #recebe a função da view
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug'] #busca a slug do curso na url
        course = get_object_or_404(Course, slug=slug) #curso atual
        has_permission = request.user.is_staff
        if not has_permission:
            try: #busco a matricula
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except Enrollment.DoesNotExist:
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição no curso ainda está pendente'
        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')
        request.course = course #td view que usar este decorator vai ter um obj curso no requestpq não quero repitir esta consulta
        return view_func(request, *args, **kwargs)
    return _wrapper
