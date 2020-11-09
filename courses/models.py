from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from core.mail import send_mail_template

class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().filter(
			Q(name__icontains=query) |
			Q(description__icontains=query)
		)  # para filtrar por um OU outro

		#Para filtrar um dado E outro
		# return self.get_queryset().filter(
		# 	name__icontains=query, description__icontains=query
		# ) #tem que ter os dois atributos, faz um lookup

class Course(models.Model):
	
	name = models.CharField('Nome',max_length = 100)
	slug = models.SlugField('Atalho')
	description = models.TextField('Descrição Simples', blank = True) #blank = não é obrigatório, mas o TextField permite descrições longas
	about = models.TextField('Sobre o Curso', blank= True)
	start_date = models.DateField('Data de Início', null = True, blank = True) #null = no banco de dados esse campo temq ter algo msm que seja um campo vazio
	#campo de imagem, caminho para a imagem
	image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null = True, blank = True)  #não é um campo obrigatório
	created_at = models.DateTimeField('Criado em', auto_now_add=True) #auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em', auto_now_add=True) #assim que for refreshed a data entra sozinha

	objects = CourseManager() #agora o manager não será o padrão do django

	def __str__(self):
		return self.name

	#@models.permalink
	def get_absolute_url(self):
		return f"/cursos/{self.slug}/"

	#consulta no banco as lições que estão liberadas até esta data
	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__gte=today) #gte maior ou igual

	class Meta: #interfere no django admin
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos' #ensinamos ao django que o plural de curso é curso
		ordering = ['name'] #comoo django organiza ascendente a lista

class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0,'Pendente'),
		(1, 'Aprovado'),
		(2,'Cancelado'),
	)

	user=models.ForeignKey(
		settings.AUTH_USER_MODEL,
		verbose_name='Usuário', on_delete = models.CASCADE,
		related_name='enrollments'
	)
	course = models.ForeignKey(
		Course, verbose_name='Curso',
		related_name='enrollments', on_delete=models.CASCADE
	)
	#indicar a situação da inscriçãodo usuário, caso a inscrição sej amoderada
	status = models.IntegerField('Situação',choices=STATUS_CHOICES, default=1, blank=True)

	created_at = models.DateTimeField('Criado em',
									  auto_now_add=True)  # auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em',
									  auto_now_add=True)  # assim que for refreshed a data entra sozinha

	#mantenha as coisas do model no model, faça as logicas de negocios aqui, não nas  views
	def activate(self): #fat model
		self.status = 1
		self.save()

	#checa se oaluno esta aprovado para este curso
	def is_approved(self):
		return self.status == 1


	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user','course'),) #evita repetição de usuario em um curso

class Announcement(models.Model):
	course = models.ForeignKey(Course,
							   verbose_name='Curso', related_name='announcements', on_delete=models.CASCADE
							   )
	title= models.CharField('Titulo', max_length=100)
	content = models.TextField('Conteúdo')
	created_at = models.DateTimeField('Criado em',auto_now_add=True)  # auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em',auto_now_add=True)  # assim que for refreshed a data entra sozinha

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at'] #sempre omaisatual primeiro

class Comment(models.Model):
	announcement = models.ForeignKey(Announcement, verbose_name='Anúncio', related_name='comments' ,on_delete= models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete= models.CASCADE)
	comment = models.TextField('Comentário')
	created_at = models.DateTimeField('Criado em',
									  auto_now_add=True)  # auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em',
									  auto_now_add=True)  # assim que for refreshed a data entra sozinha

	class Meta:
		verbose_name='Comentário'
		verbose_name_plural = 'Comentários'
		ordering =['created_at']

def post_save_announcement(instance, created, **kwargs):
	if created: #apenas se for criado
		subject = instance.title
		context = {
			'announcement': instance,
		}
		template_name = 'courses/announcement_mail.html'
		#não queremos um unico email para todos mostrando que foi copiado então:
		enrollments = Enrollment.objects.filter(course=instance.course,
												status=1
												)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)
#vamos passar ao django a função que quero q seja executado
models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement'
)#este ultimo argumento evita que cadastre uma função no sinal muitas vezes


class Lesson(models.Model):
	name = models.CharField('Nome', max_length=100)
	description = models.TextField('Descrição', blank=True)
	number = models.IntegerField('Número (ordem)', blank=True, default=0) #apenas p organizar nobackend
	release_date = models.DateField('Data de liberação', blank=True,null=True) #quando esta aula esta disponível
	#a ligação das aulas com o curso
	course = models.ForeignKey(Course, verbose_name='Curso',
							   on_delete=models.CASCADE, related_name='lessons')
	created_at = models.DateTimeField('Criado em',
									  auto_now_add=True)  # auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em',
									  auto_now_add=True)  # assim que for refreshed a data entra sozinha

	def __str__(self):
		return self.name

	#verifica se a lissão já está disponível
	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today
		return False

	class Meta:
		verbose_name = 'Aula'
		verbose_name_plural = 'Aulas'
		ordering = ['number']

#agora o conteudo/material das aulas
class Material(models.Model):
	name = models.CharField('Nome', max_length=100)
	#para colocar arquivos de multimedia, apenas o adm q cadastrará
	embedded = models.TextField('Vídeo embedded', blank=True)
	#para arquivos:
	file = models.FileField(upload_to='lessons/materials',blank=True,null=True) #o arquivo está publico
	#agora a ligação com a lição:
	lesson = models.ForeignKey(Lesson, related_name='materials', verbose_name='aula',
		on_delete=models.CASCADE)

	def is_embedded(self):
		return bool(self.embedded)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Material'
		verbose_name_plural = 'Materiais'
		#ordering = ['number']
