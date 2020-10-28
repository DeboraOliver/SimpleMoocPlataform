from django.db import models

class Course(models.Model):
	
	name = models.CharField('Nome',max_length = 100)
	slug = models.SlugField('Atalho')
	description = models.TextField('Descrição', blank = True) #blank = não é obrigatório, mas o TextField permite descrições longas
	start_date = models.DateField('Data de Início', null = True, blank = True) #null = no banco de dados esse campo temq ter algo msm que seja um campo vazio
	#campo de imagem, caminho para a imagem
	image = models.ImageField(upload_to='courses/images', verbose_name='Imagem')
	created_at = models.DateTimeField('Criado em', auto_now_add=True) #auto now toda vez q criar um curso ele coloca automaticamente a data
	updated_at = models.DateTimeField('Atualizado em', auto_now_add=True) #assim que for refreshed a data entra sozinha