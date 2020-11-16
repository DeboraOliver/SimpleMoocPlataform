#SimpleMooc

Este projeto foi desenvolvido seguindo as aulas da Udemy do prof Gileno. O curso foi desenvolvido em 2014 usando o Django 1.6, o que torna bem frustrante para qualquer aluno em 2020 que tenta seguir as explicações e os passo-a-passo.
Então, a proposta desta minha versão do simplemooc é escrever uma versão  ATUALIZADA do mesmo projeto para o Django 3.0.5. Espero que te ajude!

##O que mudou do Django 1.6 para o Django 3.0.5

Por esta já ser a segunda vez te tento fazer este curso, eu talvez não lembre todas as mudanças e adaptações que precisam ser eitas. Desta forma, caso a sua dúvida não esteja lista abaixo <ins>dê uma olhada nos arquivos!</ins> Aqui em baixo eu vou deixar alguns dos maiores problemas que eu tive. 

### Comandos básicos

Nas versões mais recentes do Django não é preciso o comando syncdb. Basta usar:

```
python manage.py makemigrations
python manage.py migrate
```
E, depois: 

```
python manage.py runserver
```
Para chamar um módulo de outro arquivo não precisa de tudo isso:

````
from simplemooc.courses.models import Course
````
Basta:
````
from courses.models import Course
````
### Erro no uso de ForeignKey no models

Fique atento e lembre se de sempre incluir o <em>on_delete</em> quando for usar a ForeignKey. Este "on_delete" diz ao django o que fazer caso a foreignkey seja apaga. Uma das vezes que o prof chama as foreignKeys é na construção do course.models:

    course = models.ForeignKey(
		Course, verbose_name='Curso',
		related_name='enrollments', on_delete=models.CASCADE
	)

### Icons (aulas 56 e 57)

Os icons devem primeiramente ser chamados no base.html (linha 9), conforme o prof mostra e os arquivos devem estar na pasta static. No meu caso, não funcionava porque eu não coloquei o arquivo na pasta static/css.
O prof usa <em>"icon-lock"</em> para chamar os icons, se não funcionar use <em>"icon fa fa-lock"</em>:
```` 
                <li>
                    <a href="{% url 'accounts:edit_password' %}">
                        <i class="icon fa fa-lock"></i>
                        Editar Senha</a>
                </li>
````                 
Na aula 57, ele mostra que há uma outra forma de chamar os icons usando <em>"fa fa-lock"</em>.

### Problemas com comentários (aula 60)

O conteúdo das videoaulas e o código que o prof deixou são diferentes. E neste caso use o código da documentação se houver problemas:

Na aula:
````
        <i class="fa fa-comments-o"></i>
            {% with comments.count=announcement.comments.count %}
            {{ comments.count }}
            Comentário{{ comments.count|pluralize }}
            {% endwith %}
        </a> 
````        
Na documentação <em>(troca-s os pontos por underline)</em>:
```` 
        <i class="fa fa-comments-o"></i>
            {% with comments_count=announcement.comments.count %}
            {{ comments_count }}
            Comentário{{ comments_count|pluralize }}
            {% endwith %}
        </a> 
```` 

### Testando a aplicação 

O comando
````
from django.core.urlresolvers import reverse
````
Foi removido na versão 2.0 do django e movido para urls. Desta forma, use o seguinte comando:
````
from django.urls import reverse
````
### Testando models com model-mommy (aula 74)
Por respeito as mulheres e para evitar esteriótipos, este pacote foi renomeado. Logo, ao invés de usar:

````
from model_mommy import mommy

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = mommy.make(...)
````
Use isto:
````
from model_bakery import baker

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = baker.make(...)
````
Aliás, não esqueça de instalar de forma correta:
````
pip install model_bakery
````

Leia mais sobre esta brilhante (e respeitosa e digna) mudança <a href = "https://pypi.org/project/model-mommy/">AQUI</a>. Conheça mais sobre o projeto model-bakery <a href = "https://pypi.org/project/model-bakery/">AQUI</a>

## Outros links legais

Alguns links que o prof menciona e que talvez, você precise em projetos futuros:

<ul>
    <li><a href = "https://fontawesome.com/?from=io">Fontawesome</a> É o fontawesome.io que o professor mostra na aula 56. Aqui você encontra o arquivo css para colocar icons no seu projeto.
</li>
    <li><a href = "https://purecss.io/">Purecss</a> Este também é mencionado na aula 56. Usado no nosso projeto no design de botões.
</li>
   
</ul> 

