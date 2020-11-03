from django.db import models
from django.db.models import Q
from django.conf import settings


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
	#indicar a situaçãoda inscriçãodo usuário, caso a inscrição sej amoderada
	status = models.IntegerField('Situação',choices=STATUS_CHOICES, default=1, blank=True)

	created_at = models.DateTimeField('Criado em',
									  auto_now_add=True)  # auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em',
									  auto_now_add=True)  # assim que for refreshed a data entra sozinha

	#mantenha as coisas do model no model, faça as logicas de negocios aqui, não nas  views
	def activate(self): #fat model
		self.status = 1
		self.save()


	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user','course'),) #evita repetição de usuario em um curso
