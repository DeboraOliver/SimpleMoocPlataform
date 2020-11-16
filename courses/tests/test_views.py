from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings #é assim que se deve chamar o settings

from courses.models import Course

#use python manage.py test

class ContactCourseTestCase(TestCase):
#com testcase td vez q rodamos os testes primeiro ele chama o set up e o terdown
    def setUp(self):#esta função cria alguma coisa
        #td vez que executar o teste ele cria este curso:
        self.course = Course.objects.create(name='Django', slug='django')

    def tearDown(self):#quandoterminar o teste
        #vms apagar o teste criado no setUp
        self.course.delete()

    # #o testcase tbm temum setupclass, onde escrevemosalgo que queremos que rode em tds os testes
    # @classmethod
    # def setUpClass(cls):
    #     pass
    #
    # #quando terminar tds os testes  dessa classe ele roda o:
    # @classmethod
    # def tearDownClass(cls):
    #     pass

    #vms criar um formulário de teste:
    def test_contact_form_error(self):
        #vms testar se dá erro qndo falta informação
        data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.') #vms ver se a falta do email faz aparecer mensagem de erro
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    #vms testar oq acontece se der td certo/houver tds as infomações requeridas no formulário
    def test_contact_form_success(self):
        data = {'name': 'Fulano de Tal', 'email': 'admin@admin.com', 'message': 'Oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)#vms testar p ver se o EMAIL é enviado
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
        #no ambiente de teste os emails ficam na outbox
        #o mail.outbox[0].to,indica que o email deve ser enviado p uma lista ([settings.CONTACT_EMAIL]), se der erro tente sem as []
        #em cima dos email posso testar o to, body, subject etc, testa assim se o assunto esta correto por exemplo