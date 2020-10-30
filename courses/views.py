from django.shortcuts import render, get_object_or_404

from .models import Course
from .forms import ContactCourse #o . indica q é nesta msm pasta

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    #o contexto é um dicionario
    #a renderização do template depende de uma contextualização q subst variareis dentro dele
    return render(request,  template_name, context)

# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     context = {
#         'courses': course
#     }
#     template_name = 'courses/details.html'
#     return render(request,  template_name, context)

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context= {}
    if request.method =='POST': #sefor um post farei algo com os dados
        form = ContactCourse(request.POST)
        if form.is_valid(): #chama a validação e verifica os dadosenvidos
            context['is_valid'] = True
            #print(form.cleaned_data['message']) #faz a diferença para usarmos apenas dados validos
            #para acessar um dado dos fform não posso fazer forms.name tenho q fazer forms.cleaned_data['']
            form = ContactCourse() #quero formulário limpo novamente
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request,  template_name, context)