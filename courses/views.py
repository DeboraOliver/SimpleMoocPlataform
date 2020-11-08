from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import  login_required
from .models import Course,  Enrollment, Announcement
from .forms import ContactCourse, CommentForm #o . indica q é nesta msm pasta
from django.contrib import messages

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
            form.send_email(course) #chama a função q esta noform
            form = ContactCourse() #quero formulário limpo novamente
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request,  template_name, context)

@login_required
def enrollment(request,slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    ) #este metodo retorna uma tuplaa inscrição e um booleano dizendo se criou ou não
    if created:
         #enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')#import messages
    else:
        messages.info(request, 'Você já está inscrito neste curso')
    return redirect('accounts:dashboard') #quando clicar em INSCREVA-SE vem para o link

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method =='POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course
    }
    return render(request, template, context)

@login_required
def announcements(request, slug):
    #vamos verificar se o aluno está inscrito no curso
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        #se ele  não estiver inscrito vamos para a segunda parte:
        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('accounts:dashboard')
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all() #todos os anuncios do curso estão nesta variável
    }
    return render(request, template, context)

@login_required
def show_announcement(request, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        # se ele  não estiver inscrito vamos para a segunda parte:
        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('accounts:dashboard')
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False) #ele vai retornar o obj mas não vai salvar por do cOMMIT=False
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'courses/show_announcement.html'
    #para evitar que ousuario manipule a url vamos especificar o anuncio do curso
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template, context)